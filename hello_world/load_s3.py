import json, boto3, io, tempfile
from pydub import AudioSegment
from typing import Dict

s3 = boto3.client('s3')
s3_bucket = 'frejorsbucket'


def load_s3_audio(bucket: str, key: str) -> str:
    # Create a temporary file
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    # Download audio from S3 into memory
    audio_data = io.BytesIO()
    s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=audio_data)

    # Reset buffer to the start
    audio_data.seek(0)

    # Write the bytes to the temporary file
    with open(temp_audio_file.name, 'wb') as f:
        f.write(audio_data.read())

    # Return the path to the temporary file
    return temp_audio_file.name


def load_s3_json(bucket: str, key: str) -> str:
    # Fetch the JSON from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    json_data = response['Body'].read().decode('utf-8')

    # Create a temporary file
    temp_json_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

    # Write the JSON data to the temporary file
    with open(temp_json_file.name, 'w') as f:
        f.write(json_data)

    # Return the path to the temporary JSON file
    return temp_json_file.name