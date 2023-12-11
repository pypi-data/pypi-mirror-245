"""
Test suite for Russell-Rao kernel.
"""

import pytest
import torch
from gpytorch.kernels import ScaleKernel

from gauche.kernels.fingerprint_kernels.russell_rao_kernel import (
    RussellRaoKernel,
    batch_russell_rao_sim,
)

tkwargs = {"dtype": torch.double}


@pytest.mark.parametrize(
    "x1, x2",
    [
        (torch.ones((2, 2), **tkwargs), torch.ones((2, 2), **tkwargs)),
    ],
)
def test_russell_rao_similarity_with_equal_inputs(x1, x2):
    """Test the Russell-Rao similarity metric between two equal input tensors."""
    similarity = batch_russell_rao_sim(x1, x2)
    assert torch.isclose(similarity, torch.ones((2, 2), **tkwargs)).all()


def test_russell_rao_similarity_with_unequal_inputs():
    """Test the Russell-Rao similarity metric between two unequal input tensors."""
    x1 = torch.tensor([1, 0, 1, 1], **tkwargs)
    x2 = torch.tensor([1, 1, 0, 0], **tkwargs)
    # Add a batch dimension
    x1 = x1[None, :]
    x2 = x2[None, :]
    similarity = batch_russell_rao_sim(x1, x2)

    assert torch.allclose(similarity, torch.tensor(1.0 / 4.0, **tkwargs))


def test_russell_rao_kernel():
    """Test the Russell-Rao kernel when integrated with GP."""

    x = torch.randint(0, 2, (10, 5))
    # Non-batch: Simple option
    covar_module = ScaleKernel(RussellRaoKernel())
    covar = covar_module(x)  # Output: LazyTensor of size (10 x 10)
    assert covar.size() == torch.Size([10, 10])
    batch_x = torch.randint(0, 2, (2, 10, 5))
    # Batch: Simple option
    covar_module = ScaleKernel(RussellRaoKernel())
    covar = covar_module(batch_x)  # Output: LazyTensor of size (2 x 10 x 10)
    assert covar.size() == torch.Size([2, 10, 10])
