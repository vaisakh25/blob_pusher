import os
import yaml
from utils.video_util import convert_stream_to_frames_and_push_to_blob

# Call the video utility function from the imported module
if __name__ == "__main__":
    # Load input parameters from YAML file
    with open('input_params.yml', 'r') as f:
        input_params = yaml.safe_load(f)

    # Convert video stream to frames and push to Azure Blob Storage
    convert_stream_to_frames_and_push_to_blob(input_params)
