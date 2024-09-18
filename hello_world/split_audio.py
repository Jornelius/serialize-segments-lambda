import math
import json
import io
import boto3
import time
from pydub import AudioSegment
from encode_audio import get_clip_buffer

# Initialize the S3 client
s3_client = boto3.client('s3')


def split_audio_into_segments(audio_file_path, diarization_dict_path):
    #     Todo use the raw_diarization_dict to get start time end time
    """
    Splits an audio file into smaller segments based on the specified segment length from the diarization dictionary.
    """

    # Load the diarization dictionary from the JSON file
    with open(diarization_dict_path, 'r') as file:
        diarization_dict = json.load(file)
    
    # Load the audio file as bytes
    with open(audio_file_path, "rb") as audio_file:
        file_bytes = audio_file.read()
    
    # Load the audio file as an AudioSegment
    sound = AudioSegment.from_file(io.BytesIO(file_bytes), format="mp3")
    
    # Initialize variables
    audio_buffer_list = []
    start_time_list = []
    end_time_list = []
    total_clipping_time = 0
    n_sentences = len(diarization_dict)
    
    # Iterate over diarization segments
    for i, segment_dict in diarization_dict.items():
        start_time = segment_dict["start"]
        end_time = segment_dict["end"]

        # Append start and end times to lists
        start_time_list.append(start_time)
        end_time_list.append(end_time)

        # Measure time to get audio segment
        st_get_clip = time.perf_counter()
        segment = get_clip_buffer(sound, start_time, end_time, target_audio_format="mp3")
        et_get_clip = time.perf_counter()
        get_clip_time = et_get_clip - st_get_clip

        # Update total clipping time and add audio buffer to the list
        total_clipping_time += get_clip_time
        audio_buffer_list.append(segment)

    return audio_buffer_list