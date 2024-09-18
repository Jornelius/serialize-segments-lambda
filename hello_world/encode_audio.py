import io
import base64
from pydub import AudioSegment

def encode_audio_segment(audio_segment: AudioSegment) -> str:
    """
    Encodes an AudioSegment object to a base64-encoded string.
    """
    buffer = io.BytesIO()
    audio_segment.export(buffer, format="mp3")  # Export as MP3 format
    encoded_audio = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Encode and convert to string
    return encoded_audio

def encode_audio_buffers(audio_buffers: list) -> list:
    """
    Encodes a list of io.BytesIO audio buffers to base64-encoded strings.

    Parameters:
    - audio_buffers (list): List of io.BytesIO objects containing audio data.

    Returns:
    - list: List of base64-encoded audio strings.
    """
    encoded_audio_list = []
    for audio_buffer in audio_buffers:
        audio_segment = AudioSegment.from_file(audio_buffer, format="mp3")  # Load audio segment
        encoded_audio = encode_audio_segment(audio_segment)  # Encode to base64
        encoded_audio_list.append(encoded_audio)
    return encoded_audio_list


def get_clip_buffer(original_sound_bytes: bytes,
                    start_time: int,
                    end_time: int,
                    source_audio_format: str = None,
                    target_audio_format: str = "mp3",
                    target_nbr_of_channels: int = 1) -> bytes:
    """
       Extracts a portion of audio, adjusts its channels, and returns the result as a bytes buffer.

       Parameters:
       - original_sound_bytes (bytes): The binary representation of the original audio.
       - start_time (float): The starting time for extracting audio in seconds.
       - end_time (float): The ending time for extracting audio in seconds.
       - source_audio_format (str, optional): The format of the source audio file. If None, assumes original_sound_bytes is in the desired format.
       - target_audio_format (str, optional): The desired format for the target audio. Default is "wav".
       - target_nbr_of_channels (int, optional): The desired number of channels for the target audio. Default is 1.

       Returns:
       - io.BytesIO: A bytes buffer containing the modified audio data in the specified format.

       Usage:
       This function is designed to extract a segment of audio, adjust its channels, and return the result as a bytes buffer.
       If source_audio_format is provided, it loads the audio from the bytes using the specified format; otherwise, it assumes original_sound_bytes is in the desired format.
       The extracted audio is trimmed based on start_time and end_time, and its number of channels is set to target_nbr_of_channels.
       The modified audio is then exported to a bytes buffer in the specified target_audio_format, and the buffer is returned.

       """
    if source_audio_format is not None:
        # AudioSegment is capable of reading a file directly from the bytes (using a stream)
        sound = AudioSegment.from_file(io.BytesIO(original_sound_bytes), source_audio_format)
    else:
        sound = original_sound_bytes

    sound = sound[start_time * 1000: end_time * 1000]  # times must be in milliseconds
    sound = sound.set_channels(target_nbr_of_channels)  # embeddings are calculated from 1D audio files

    sound_buffer = io.BytesIO()
    sound.export(sound_buffer, format=target_audio_format)

    return sound_buffer