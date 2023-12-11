import torch
import numpy as np


def test_preprocessing(pretrained_interface):
    loaded_image = np.random.rand(100, 100, 3).astype(np.uint8)
    pretrained_interface=pretrained_interface()
    assert (
        isinstance(
            pretrained_interface.data_preprocessing(loaded_image), torch.FloatTensor
        )
        is True
    )

def test_postprocessing(pretrained_interface):
    loaded_image = np.random.rand(100, 100, 3).astype(np.uint8)
    pretrained_interface=pretrained_interface()
    assert isinstance(
        pretrained_interface.data_postprocessing(
            torch.ones((1,512, 512), dtype=torch.float64), loaded_image
        ),
        np.ndarray,
    )


def test_seg(loaded_image, pretrained_interface):
    pretrained_interface=pretrained_interface()
    assert isinstance(
        pretrained_interface(loaded_image),
        np.ndarray,
    )
