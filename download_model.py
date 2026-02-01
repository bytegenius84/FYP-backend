import os
import requests

# Path where the model will be saved
MODEL_PATH = "models/nutrifoodnet_final.h5"

# Google Drive file ID (from your link)
FILE_ID = "1ho8wwkADHIVGj1Iq5614A3h7uqbhkrTC"

# Download URL for Google Drive large files
DOWNLOAD_URL = "https://docs.google.com/uc?export=download"

def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs("models", exist_ok=True)
        print("Downloading model from Google Drive...")

        session = requests.Session()
        response = session.get(DOWNLOAD_URL, params={'id': FILE_ID}, stream=True)
        
        # Check for confirmation token (for large files)
        token = get_confirm_token(response)
        if token:
            params = {'id': FILE_ID, 'confirm': token}
            response = session.get(DOWNLOAD_URL, params=params, stream=True)

        save_response_content(response, MODEL_PATH)
        print("Model downloaded successfully.")
    else:
        print("Model already exists.")

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)
