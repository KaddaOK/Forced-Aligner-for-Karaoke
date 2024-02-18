from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
from pydub import AudioSegment
import magic
import soundfile as sf
import json

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--audiofile", required=True, help="path of the vocal audio file")
parser.add_argument("-l", "--lyricsfile", required=True, help="path of the lyrics text file")
parser.add_argument("-p", "--append_pipe", default=True, help="add a pipe character to the end of each lyric line")
args = vars(parser.parse_args())

def detect_audio_format(file_path):
    mime_type = magic.Magic(mime=True).from_file(file_path)
    if mime_type == 'audio/x-wav':
        return 'wav'
    elif mime_type == 'audio/flac':
        return 'flac'
    elif mime_type == 'audio/mpeg':
        return 'mp3'
    # Add more mime types as needed
    else:
        raise ValueError("Unsupported audio format")

print(f"Preparing audio...")   

fullaudiopath = os.path.abspath(args["audiofile"])

format = detect_audio_format(fullaudiopath)

print(f" * Input format is {format}.")

# Load the audio file
sound = AudioSegment.from_file(fullaudiopath, format=format)

RESAMPLED_FILE_NAME = f"{fullaudiopath}.prepared.wav"
# Downmix to mono if stereo
if sound.channels == 2:
    print(f" * Input is stereo; need to downmix to mono.")
    sound = sound.set_channels(1)

# Resample to 16000 Hz if higher
if sound.frame_rate > 16000:
    print(f" * Input is {sound.frame_rate} Hz, need to resample to 16000 Hz")
    sound = sound.set_frame_rate(16000)

# Export the processed audio
print(f" * Exporting to {RESAMPLED_FILE_NAME}")
sound.export(RESAMPLED_FILE_NAME, format="wav")

# Open the text file and read its contents
with open(args["lyricsfile"]) as f:
    # Read the file contents
    lines = f.readlines()

# Remove blank lines and unwanted characters
cleaned_lines = [
    line.strip().replace(',', '').replace('.', '').replace('!', '').replace('?', '')
    for line in lines
    if line.strip()  # Filter out blank lines
]

# Append " |" to each valid line if append_pipe is True
if args["append_pipe"]:
    cleaned_lines = [line + " |" for line in cleaned_lines]

# Join the cleaned lines into a single string
cleaned_text = '\n'.join(cleaned_lines)

#write the manifest
manifest_filepath = f"{fullaudiopath}.manifest.json"
manifest_data = {
    "audio_filepath": f"{RESAMPLED_FILE_NAME}",
    "text": cleaned_text
}

print (f"Writing manifest to {manifest_filepath}")
with open(manifest_filepath, 'w') as f:
  line = json.dumps(manifest_data)
  f.write(line + "\n")