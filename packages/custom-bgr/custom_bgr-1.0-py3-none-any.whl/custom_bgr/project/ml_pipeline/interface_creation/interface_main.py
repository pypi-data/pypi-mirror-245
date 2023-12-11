import numpy as np
import cv2

class InterfaceMain():
    """
    Main Interface class for handling segmentation models.

    Attributes:
    - seg_model: Segmentation model instance.
    - device (str): Device on which the model is run ('cpu' or 'cuda').
    """

    def __init__(self, seg_model, device):
        """
        Initialize the InterfaceMain.

        Args:
        - seg_model: Segmentation model instance.
        - device (str): Device on which the model is run ('cpu' or 'cuda').
        """
        self.seg_model = seg_model
        self.device = device

    def __call__(self, image):
        """
        Perform segmentation on the input image and return the image with an alpha channel.

        Args:
        - image (numpy.ndarray): Input image for segmentation.

        Returns:
        - numpy.ndarray: Resultant image with an alpha channel.
        """

        # Perform segmentation using the provided model
        mask = self.seg_model(image)

        # Convert the mask to uint8
        mask = mask.astype(np.uint8)

        # Resize the mask to match the original image dimensions
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

        # Create an empty alpha channel
        alpha = np.ones_like(mask, dtype=image.dtype) * 255

        # Set the alpha channel based on the mask
        alpha[mask == 0] = 0

        # Add the alpha channel to the image
        image_with_alpha = cv2.merge((image, alpha))

        print('Analysis done.')

        return image_with_alpha
