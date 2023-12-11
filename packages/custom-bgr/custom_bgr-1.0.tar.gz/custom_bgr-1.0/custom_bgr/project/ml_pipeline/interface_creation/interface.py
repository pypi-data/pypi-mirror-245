import warnings
from ml_pipeline.wrapper.u2net_pretrained import U2NETPretrained
from ml_pipeline.wrapper.u2net_custom import U2NETCustom
from ml_pipeline.interface_creation.interface_main import InterfaceMain
from collections import defaultdict


class SegInterface(InterfaceMain):
    """
    Segmentation Interface class that serves as a wrapper around U2NET models.
    This will actually be a build class which will call the main interface at the time of inferencing

    Attributes:
    - model_type (str): Type of segmentation model ('pretrained' or 'custom').
    - seg_mask_size (int): Size of the segmentation mask.
    - device (str): Device on which the model is run ('cpu' or 'cuda').
    - u2net (U2NETPretrained or U2NETCustom): Instance of the U2NET model based on 'model_type'.
    """

    def __init__(self, data):
        """
        Initialize the Segmentation Interface.

        Args:
        - data (dict): Dictionary containing information about the segmentation model.
        """

        # Ensure that 'data' is a defaultdict for graceful handling of missing keys
        data = defaultdict(lambda: None, data)

        # Define and initialize attributes based on the provided data
        self.model_type = data.get("segmentationModel")
        self.seg_mask_size = data.get("seg_mask_size")
        self.device = data.get("device")

        # Initialize 'u2net' based on the specified model type
        if self.model_type == "pretrained":
            self.u2net = U2NETPretrained(
                device=self.device,
                input_image_size=self.seg_mask_size
            )
        elif self.model_type == "custom":
            self.u2net = U2NETCustom(
                device=self.device,
                input_image_size=self.seg_mask_size
            )
        else:
            warnings.warn(
                f"Unknown model type: {self.model_type}. Using default model type: pretrained"
            )
            self.u2net = U2NETPretrained(
                _device=self.device,
                input_image_size=self.seg_mask_size
            )

        # Call the superclass constructor with the initialized 'u2net' and 'device'
        super(SegInterface, self).__init__(
            seg_model=self.u2net,
            device=self.device,
        )
