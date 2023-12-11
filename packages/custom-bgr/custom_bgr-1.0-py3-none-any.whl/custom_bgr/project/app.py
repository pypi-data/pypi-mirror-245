from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import cv2
import base64
import numpy as np
from ml_pipeline.interface_creation.interface import SegInterface
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI()

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define a Pydantic model for input data validation
class InputData(BaseModel):
    data: dict = Field(..., example={
        "model_type": "pretrained",
        "seg_mask_size": 320,
        "device": "cuda",
        "update_model": False
    })
    image: str = Field(..., example="base64ImageString")

# Global variable to store the SegInterface instance
global_interface = None

# Function to create and return a SegInterface instance
def call_interface(input_data):
    """
    Creates and returns a SegInterface instance based on input data.

    Args:
    - input_data (dict): Input data for creating the SegInterface.

    Returns:
    - SegInterface: Instance of the SegInterface class.
    """
    interface = SegInterface(input_data)
    return interface

# Function to process the image and return the result
def process_image(image_data, interface):
    """
    Processes the input image using the provided SegInterface instance.

    Args:
    - image_data (str): Base64 encoded image string.
    - interface (SegInterface): Instance of the SegInterface class.

    Returns:
    - str: Base64 encoded result image string.
    """
    # Decode the base64 image
    image_data = image_data.split(",")[-1]
    image_bytes = base64.b64decode(image_data)
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    # Check the number of channels in the image
    num_channels = image.shape[2] if len(image.shape) == 3 else 1

    # If the image has only one channel, convert it to 3 channels
    if num_channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # Your processing logic here, i.e we can use SegInterface to process the image
    result_image = interface(image)
    # Encode the result image as base64
    _, buffer = cv2.imencode('.png', result_image)
    result_image_base64 = base64.b64encode(buffer).decode('utf-8')

    return result_image_base64

# FastAPI endpoint to analyze the image
@app.post("/process")
async def analyze_image(input_data: InputData):
    """
    FastAPI endpoint for processing the input image.

    Args:
    - input_data (InputData): Pydantic model for input data.

    Returns:
    - dict: Result containing the base64 encoded image.
    """
    global global_interface
    try:
        # Create or update the SegInterface instance
        global_interface = call_interface(input_data.data)
        # Process the image using the SegInterface instance
        result_image_base64 = process_image(input_data.image, global_interface)
        return {"image": result_image_base64}
    except Exception as e:
        print('error-----', e)
        raise HTTPException(status_code=500, detail=str(e))

# Start the FastAPI application
print('APP started')

# Note: The following block is typically used for running the application with uvicorn
# Uncomment it if you intend to run the application as a standalone script
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="192.168.1.45", port=8000)
