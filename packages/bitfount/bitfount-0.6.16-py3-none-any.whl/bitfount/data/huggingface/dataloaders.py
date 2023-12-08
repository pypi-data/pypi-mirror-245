"""HuggingFace compatible dataloaders."""
import random
import secrets
from typing import Iterator, List

import torch

from bitfount.backends.pytorch import (
    PyTorchBitfountDataLoader,
    PyTorchIterableBitfountDataLoader,
)
from bitfount.backends.pytorch.data.utils import _convert_batch_to_tensor
from bitfount.data.huggingface.datasets import (
    _HuggingFaceDataset,
    _IterableHuggingFaceDataset,
)
from bitfount.data.types import _DataBatch, _SingleOrMulti
from bitfount.utils import delegates


@delegates()
class HuggingFaceBitfountDataLoader(PyTorchBitfountDataLoader):
    """Wraps a PyTorch DataLoader with bitfount functions.

    Args:
       dataset: An pytorch compatible dataset.
    """

    dataset: _HuggingFaceDataset


@delegates()
class HuggingFaceIterableBitfountDataLoader(PyTorchIterableBitfountDataLoader):
    """Wraps a PyTorch DataLoader with bitfount functions.

    Args:
       dataset: An HuggingFace compatible dataset.
    """

    dataset: _IterableHuggingFaceDataset

    @staticmethod
    def convert_input_target(batch: _DataBatch) -> List[_SingleOrMulti[torch.Tensor]]:
        """Convert the input and target to match the hugging face expected inputs_."""
        input_, target_ = _convert_batch_to_tensor(batch)
        if isinstance(input_, list):
            input_ = torch.stack(input_)
            input_ = torch.swapaxes(input_, 0, 1)
        return [input_, target_]

    def __iter__(self) -> Iterator[List[_SingleOrMulti[torch.Tensor]]]:
        """Yields a batch of data when iterated.

        We use a custom iterator with different behaviour depending on whether the
        dataset should be shuffled or not. Each batch is explicitly converted to torch
        tensors prior to yielding as this is not done automatically by pytorch.
        """
        batch: _DataBatch = []

        if self.shuffle:
            # If the dataset should be shuffled, we use a reservoir sampling method
            # to sample from a buffer of elements from the dataset.
            buffer_: _DataBatch = []
            for sample in self.dataset:
                if len(batch) == self.batch_size:
                    yield self.convert_input_target(batch)
                    batch = []

                if len(buffer_) == self.buffer_size:
                    if self.secure_rng:
                        idx = secrets.randbelow(self.buffer_size)
                    else:
                        # Ignoring security warning here because RNG does not need
                        # to be cryptographically secure if it is turned off by
                        # the user.
                        idx = random.randint(
                            0, self.buffer_size - 1
                        )  # nosec B311 # "random" usage
                    batch.append(buffer_[idx])
                    buffer_[idx] = sample
                else:
                    buffer_.append(sample)

            # This is only reached once the dataset iterator has been exhausted. The
            # remainder of the buffer is shuffled and yielded until empty.
            random.shuffle(buffer_)
            while buffer_:
                if len(batch) == self.batch_size:
                    yield self.convert_input_target(batch)
                    batch = []

                batch.append(buffer_.pop())
        else:
            # If the dataset should not be shuffled, we simply iterate over the dataset
            for sample in self.dataset:
                if len(batch) == self.batch_size:
                    yield self.convert_input_target(batch)
                    batch = []

                batch.append(sample)

        # If there are any elements left in the batch after the dataset/buffer are
        # empty, yield an incomplete batch.
        if batch:
            yield self.convert_input_target(batch)
