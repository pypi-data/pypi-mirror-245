import torch
import numpy as np


def test_preprocessing(custom_interface):
    custom_interface=custom_interface()
    loaded_image = np.random.rand(100, 100, 3).astype(np.uint8)
    assert (
        isinstance(
            custom_interface.preprocess_img(loaded_image), np.ndarray
        )
        is True
    )

def test_postprocessing(custom_interface):
    custom_interface=custom_interface()
    loaded_image = np.random.rand(100, 100, 3).astype(np.uint8)
    loaded_mask = np.random.rand(100, 100, 3).astype(np.uint8)
    assert isinstance(
        custom_interface.postprocess_mask(loaded_mask,loaded_image
        ),
        np.ndarray,
    )


def test_seg(loaded_image, custom_interface):
    custom_interface=custom_interface()
    assert isinstance(
        custom_interface(loaded_image),
        np.ndarray,
    )
