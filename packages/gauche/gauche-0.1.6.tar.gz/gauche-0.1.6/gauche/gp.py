from copy import copy, deepcopy
from functools import lru_cache

import torch
from gpytorch import settings
from gpytorch.distributions import MultivariateNormal
from gpytorch.likelihoods import _GaussianLikelihoodBase
from gpytorch.models import ExactGP
from gpytorch.models.exact_prediction_strategies import prediction_strategy


class NonTensorialInputs:
    def __init__(self, data):
        self.data = data

    def append(self, new_data):
        self.data.extend(new_data.data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def __deepcopy__(self, memo):
        return NonTensorialInputs(copy(self.data))


class SIGP(ExactGP):
    """
    A reimplementation of gpytorch's ExactGP that allows for non-tensorial inputs.
    The inputs to this class may be a gauche.NonTensorialInputs instance, with graphs
    stored within the object's .data attribute.

    In the longer term, if ExactGP can be refactored such that the validation checks ensuring
    that the inputs are torch.Tensors are optional, this class should subclass ExactGP without
    performing those checks.
    """

    def __init__(self, train_inputs, train_targets, likelihood):
        if (
            train_inputs is not None
            and type(train_inputs) is NonTensorialInputs
        ):
            train_inputs = (train_inputs,)
        if not isinstance(likelihood, _GaussianLikelihoodBase):
            raise RuntimeError("SIGP can only handle Gaussian likelihoods")

        super(ExactGP, self).__init__()
        if train_inputs is not None:
            self.train_inputs = tuple(
                i.unsqueeze(-1)
                if torch.is_tensor(i) and i.ndimension() == 1
                else i
                for i in train_inputs
            )
            self.train_targets = train_targets
        else:
            self.train_inputs = None
            self.train_targets = None
        self.likelihood = likelihood

        self.prediction_strategy = None

    def __call__(self, *args, **kwargs):
        train_inputs = (
            list(self.train_inputs) if self.train_inputs is not None else []
        )

        inputs = [
            i.unsqueeze(-1)
            if torch.is_tensor(i) and i.ndimension() == 1
            else i
            for i in args
        ]

        # Training mode: optimizing
        if self.training:
            if self.train_inputs is None:
                raise RuntimeError(
                    "train_inputs, train_targets cannot be None in training mode. "
                    "Call .eval() for prior predictions, or call .set_train_data() to add training data."
                )
            res = super(ExactGP, self).__call__(*inputs, **kwargs)
            return res

        # Prior mode
        elif (
            settings.prior_mode.on()
            or self.train_inputs is None
            or self.train_targets is None
        ):
            full_inputs = args
            full_output = super(ExactGP, self).__call__(*full_inputs, **kwargs)
            if settings.debug().on():
                if not isinstance(full_output, MultivariateNormal):
                    raise RuntimeError(
                        "SIGP.forward must return a MultivariateNormal"
                    )
            return full_output

        # Posterior mode
        else:
            # Get the terms that only depend on training data
            if self.prediction_strategy is None:
                train_output = super(ExactGP, self).__call__(
                    *train_inputs, **kwargs
                )

                # Create the prediction strategy for
                self.prediction_strategy = prediction_strategy(
                    train_inputs=train_inputs,
                    train_prior_dist=train_output,
                    train_labels=self.train_targets,
                    likelihood=self.likelihood,
                )

            # Concatenate the input to the training input
            full_inputs = []
            if torch.is_tensor(train_inputs[0]):
                batch_shape = train_inputs[0].shape[:-2]
                for train_input, input in zip(train_inputs, inputs):
                    # Make sure the batch shapes agree for training/test data
                    if batch_shape != train_input.shape[:-2]:
                        batch_shape = torch.broadcast_shapes(
                            batch_shape, train_input.shape[:-2]
                        )
                        train_input = train_input.expand(
                            *batch_shape, *train_input.shape[-2:]
                        )
                    if batch_shape != input.shape[:-2]:
                        batch_shape = torch.broadcast_shapes(
                            batch_shape, input.shape[:-2]
                        )
                        train_input = train_input.expand(
                            *batch_shape, *train_input.shape[-2:]
                        )
                        input = input.expand(*batch_shape, *input.shape[-2:])
                    full_inputs.append(torch.cat([train_input, input], dim=-2))
            else:
                # from IPython.core.debugger import set_trace; set_trace()
                full_inputs = deepcopy(train_inputs)
                full_inputs[0].append(inputs[0])

            # Get the joint distribution for training/test data
            full_output = super(ExactGP, self).__call__(*full_inputs, **kwargs)
            if settings.debug().on():
                if not isinstance(full_output, MultivariateNormal):
                    raise RuntimeError(
                        "SIGP.forward must return a MultivariateNormal"
                    )
            full_mean, full_covar = (
                full_output.loc,
                full_output.lazy_covariance_matrix,
            )

            # Determine the shape of the joint distribution
            batch_shape = full_output.batch_shape
            joint_shape = full_output.event_shape
            tasks_shape = joint_shape[1:]  # For multitask learning
            test_shape = torch.Size(
                [
                    joint_shape[0] - self.prediction_strategy.train_shape[0],
                    *tasks_shape,
                ]
            )

            # Make the prediction
            with settings.cg_tolerance(settings.eval_cg_tolerance.value()):
                (
                    predictive_mean,
                    predictive_covar,
                ) = self.prediction_strategy.exact_prediction(
                    full_mean, full_covar
                )

            # Reshape predictive mean to match the appropriate event shape
            predictive_mean = predictive_mean.view(
                *batch_shape, *test_shape
            ).contiguous()
            return full_output.__class__(predictive_mean, predictive_covar)
