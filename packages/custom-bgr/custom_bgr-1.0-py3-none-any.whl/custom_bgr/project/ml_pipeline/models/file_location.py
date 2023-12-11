import os
import requests

# Note we will be downloading the models from out github releases directly inside our containers where app is running.

def download_model(model_url, save_path):
    """
    Downloads a model from the given URL and saves it to the specified path.

    Parameters:
    - model_url (str): URL of the model to be downloaded.
    - save_path (str): File path to save the downloaded model.
    """
    if os.path.exists(save_path):
        print(f"Model already exists at: {save_path}. Skipping download.")
        return

    # Make a request to the GitHub URL
    response = requests.get(model_url, stream=True)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Create the model folder if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the content to the specified file path
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)

        print(f"Model downloaded successfully and saved at: {save_path}")
    else:
        print(f"Failed to download the model. Status code: {response.status_code}")

def u2net_full_pretrained(download: bool):
    """
    Returns the location of the u2net pretrained model.

    Parameters:
    - download (bool): If True, download the model; if False, return the path without downloading.

    Returns:
        pathlib.Path: Path to the model location.
    """
    selected_model = "u2net_pretrained.pth"

    model_url = "https://github.com/Rishabh20539011/Custom_BGR_APP/releases/download/v1.0.0/u2net_pretrained.pth"

    # Replace this path with the desired location to save the model file
    save_path = os.path.join(os.path.dirname(__file__), "model_folder", selected_model)

    if download:
        download_model(model_url, save_path)
    return save_path

def u2net_full_custom(download: bool):
    """
    Returns the location of the custom u2net model.

    Parameters:
    - download (bool): If True, download the model; if False, return the path without downloading.

    Returns:
        pathlib.Path: Path to the model location.
    """
    selected_model = "u2net_custom.pt"

    model_url = "https://github.com/Rishabh20539011/Custom_BGR_APP/releases/download/v1.0.0/u2net_custom.pt"

    # Replace this path with the desired location to save the model file
    save_path = os.path.join(os.path.dirname(__file__), "model_folder", selected_model)

    if download:
        download_model(model_url, save_path)
    return save_path

def download_all():
    """
    Downloads both pretrained and custom u2net models.
    """
    u2net_full_pretrained(download=True)
    u2net_full_custom(download=True)

