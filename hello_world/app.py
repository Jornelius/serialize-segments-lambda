import boto3
import json
from split_audio import split_audio_into_segments
from load_s3 import load_s3_json, load_s3_audio
from encode_audio import encode_audio_buffers

# Initialize S3 client
s3 = boto3.client('s3')

# Process and upload audio
def lambda_handler(event, context):
    """
    Load a large audio file, split it into segments, encode each segment to base64,
    serialize the segments to JSON, and upload to S3.

    Args:
        audio_file_path (str): Path to the large audio file.
        bucket_name (str): Name of the S3 bucket.
        s3_key (str): Key path in the S3 bucket where the JSON will be stored.
    """
    raw_diarization_dict = load_s3_json('serializesegmentsbucket', 'raw_diarization.json')
    audio_file = load_s3_audio('serializesegmentsbucket', 'audio.mp3')

    # Split the audio into segments
    audio_buffer_list = split_audio_into_segments(audio_file, raw_diarization_dict)

    # Encode each segment to base64 so we can serialize it
    encoded_audio_list = encode_audio_buffers(audio_buffer_list)

    print(encoded_audio_list[0])

    # Serialize the list of base64-encoded audio segments to JSON
    serialized_audio_segments = json.dumps(encoded_audio_list)

    # Upload the JSON string to S3
    s3.put_object(
        Bucket='frejorsbucket',
        Key='serialized_audio.json',
        Body=serialized_audio_segments,
        ContentType='application/json'
    )

    print(f"Serialized audio segments saved to s3://{'frejorsbucket'}/{'serialized_audio'}")