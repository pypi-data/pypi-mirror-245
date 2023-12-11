import numpy as np
import torch
import cv2
from custom_bgr.project.ml_pipeline.architecture.u2net_pretrained_arch import U2NETArchitecture
from custom_bgr.project.ml_pipeline.models.file_location import u2net_full_pretrained

__all__ = ["U2NET"]


class U2NETPretrained(U2NETArchitecture):
    """U^2-Net model interface"""

    def __init__(
        self,
        layers_cfg="full",
        device="cpu",
        input_image_size:int = 512,
    ):
        """
        Initialize the U2NET model

        Args:
            layers_cfg: neural network layers configuration
            device: processing device
            input_image_size: input image size

        """
        super(U2NETPretrained, self).__init__(cfg_type=layers_cfg, out_ch=1)
        self.device = device
        self.model_path=u2net_full_pretrained(download=False)
        self.input_image_size = (input_image_size, input_image_size)
        self.to(device)
        
        self.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.eval()

    def data_preprocessing(self, image):
        """
        Transform input image to suitable data format for neural network

        Args:
            data: input image

        Returns:
            input for neural network

        """

        image = cv2.resize(image, (320, 320), cv2.INTER_AREA)
        image = image.astype('float64')
        temp_image = np.zeros((image.shape[0], image.shape[1], 3))

        if np.max(image) != 0:
            image /= np.max(image)
        temp_image[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
        temp_image[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
        temp_image[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225
        temp_image = temp_image.transpose((2, 0, 1))
        temp_image = np.expand_dims(temp_image, 0)

        return torch.from_numpy(temp_image).type(torch.FloatTensor)

    @staticmethod
    def data_postprocessing(data, original_image):
        """
        Transforms output data from neural network to suitable data
        format for using with other components of this framework.

        Args:
            data: output data from neural network
            original_image: input image which was used for predicted data

        Returns:
            Segmentation mask as PIL Image instance

        """
        data = data.unsqueeze(0)
        mask = data[:, 0, :, :]
        ma = torch.max(mask)  # Normalizes prediction
        mi = torch.min(mask)
        predict = ((mask - mi) / (ma - mi)).squeeze()

        print('predict pretrained---',predict.shape)

        predict_np = predict.cpu().data.numpy() * 255
        # mask = Image.fromarray(predict_np).convert("L")
        mask = cv2.resize(predict_np, (original_image.shape[1], original_image.shape[0]))

        return mask


    def __call__(self, actual_image):
        """
        Passes input images though neural network and returns segmentation masks as PIL.Image.Image instances

        Args:
            images: input images

        Returns:
            segmentation masks as for input images, as PIL.Image.Image instances

        """
        image=self.data_preprocessing(actual_image)
        with torch.no_grad():
            image =image.to(self.device)
            mask, d2, d3, d4, d5, d6, d7 = super(U2NETPretrained, self).__call__(image)
            mask_cpu = mask.cpu()
            new_mask=self.data_postprocessing(mask_cpu,actual_image)
            return new_mask

