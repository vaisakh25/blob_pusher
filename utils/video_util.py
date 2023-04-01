import os
import cv2
import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import time

def convert_stream_to_frames_and_push_to_blob(input_params):
    # Get input parameters from YAML file
    stream_url = input_params['stream_url']
    account_name = input_params['account_name']
    account_key = input_params['account_key']
    container_name_template = input_params['container_name_template']
    blob_name_template = input_params['blob_name_template']

    # Connect to Azure Storage account
    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key
    )

    # Set up container and blob clients
    now = datetime.datetime.now()
    container_name = now.strftime(container_name_template)
    container_client = blob_service_client.get_container_client(container_name)

    # Set up video capture object
    cap = cv2.VideoCapture(stream_url)

    # Loop over frames in the video stream
    while True:
        # Capture a frame
        ret, frame = cap.read()

        # If the frame could not be captured, break out of the loop
        if not ret:
            break

        # Convert the frame to JPEG format
        success, jpeg_frame = cv2.imencode('.jpg', frame)
        if not success:
            continue

        # Get the current date and time
        now = datetime.datetime.now()

        # Construct the name of the blob to store the frame in
        blob_name = now.strftime(blob_name_template)

        # Create a blob client for the new blob
        blob_client = container_client.get_blob_client(blob_name)

        # Upload the frame as a blob
        blob_client.upload_blob(jpeg_frame.tobytes())

        # Sleep for a specified amount of time (if desired)
        time.sleep(1)

    # Release the video capture object and close the container client
    cap.release()
    container_client.close()
