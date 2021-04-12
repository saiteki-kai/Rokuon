import os
from hurry.filesize import size
import audioread


def get_file_duration(filepath):
    with audioread.audio_open(filepath) as file:
        length = int(file.duration)

        hours = length // 3600
        length %= 3600
        mins = length // 60
        length %= 60
        seconds = length

        return f"{hours:02}:{mins:02}:{seconds:02}"


def get_file_size(filepath):
    bytes_size = os.path.getsize(filepath)
    return size(bytes_size)
