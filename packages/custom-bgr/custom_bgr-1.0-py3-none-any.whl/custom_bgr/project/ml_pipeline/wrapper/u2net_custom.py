import numpy as np
import torch
import cv2
from custom_bgr.project.ml_pipeline.architecture.u2net_custom_arch import U2NETArch
from custom_bgr.project.ml_pipeline.models.file_location import u2net_full_custom

class U2NETCustom(U2NETArch):
    """
    U2NETCustom class is a custom implementation of U2NET architecture.
    It inherits from U2NETArch and includes additional functionalities.
    """

    def __init__(self, device="cpu", input_image_size: int = 512):
        """
        Constructor for U2NETCustom.

        Parameters:
        - device (str): Device on which the model will be loaded ('cpu' or 'cuda').
        - input_image_size (int): Size to which the input image will be resized.

        Attributes:
        - _device (str): Device on which the model is loaded.
        - model_path (str): Path to the pre-trained model weights file.
        - input_image_size (int): Size to which the input image will be resized.
        """
        super(U2NETCustom, self).__init__(arch="UnetPlusPlus", encoder_name="timm-efficientnet-b5", in_channels=3,
                                          out_classes=1, decoder_attention_type='scse')

        self._device = device
        self.model_path = u2net_full_custom(download=False)
        self.input_image_size = input_image_size
        self.to(self._device)

        # Loading the saved model weights
        self.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.eval()

    def preprocess_img(self, image):
        """
        Preprocess the input image.

        Parameters:
        - image (numpy.ndarray): Input image as a NumPy array.

        Returns:
        - numpy.ndarray: Preprocessed image.
        """
        # Resizing
        image = cv2.resize(image, (int(self.input_image_size), int(self.input_image_size)), cv2.INTER_AREA)
        
        # Transposing
        image = image.transpose(2, 0, 1)
        return image

    @staticmethod
    def postprocess_mask(mask, image):
        """
        Postprocess the predicted mask.

        Parameters:
        - mask (numpy.ndarray): Predicted mask.
        - image (numpy.ndarray): Original image.

        Returns:
        - numpy.ndarray: Postprocessed mask.
        """
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
        return mask

    def __call__(self, actual_image):
        """
        Perform the inference on the input image.

        Parameters:
        - actual_image (numpy.ndarray): Original input image.

        Returns:
        - numpy.ndarray: Predicted mask.
        """
        print('image shape----initial ', actual_image.shape)

        image = self.preprocess_img(actual_image)
        # Adding one more dimension in front
        image = torch.unsqueeze(torch.tensor(image), 0).to(self._device)

        result = super(U2NETCustom, self).forward(image)
        print('predict custom---', result.shape)

        sigmoid_res = np.array(result.sigmoid().detach().cpu())
        sigmoid_res[sigmoid_res > 0.5] = 255
        sigmoid_res[sigmoid_res != 255] = 0
        final_mask = sigmoid_res.astype("uint8")[0][0]
        final_mask = self.postprocess_mask(mask=final_mask, image=actual_image)

        return final_mask
