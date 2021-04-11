def get_file_duration(filepath):
	import audioread

	with audioread.audio_open(filepath) as f:
		length = int(f.duration)

		hours = length // 3600
		length %= 3600
		mins = length // 60
		length %= 60
		seconds = length

		return f"{hours:02}:{mins:02}:{seconds:02}"


def get_file_size(filepath):
	import os
	from math import log2

	suffixes = ['bytes', 'KB', 'MB', 'GB']
	size = os.path.getsize(filepath)
	
	order = int(log2(size) / 10) if size else 0
	return '{:.4g} {}'.format(size / (1 << (order * 10)), suffixes[order])
