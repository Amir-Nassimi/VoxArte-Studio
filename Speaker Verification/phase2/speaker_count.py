import os
import re
import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument("--inp", help="data directory containing sound files")
args = parser.parse_args()


def extract_speaker_id(filename):
    match = re.match(r'^(\d+)-', filename)  
    if match:
        return match.group(1) 
    return None

directory_speaker_count = defaultdict(set)  
speaker_file_count = defaultdict(int) 

for root, _, files in os.walk(args.inp):
    directory_name = os.path.basename(root)
    for file in files:
        speaker_id = extract_speaker_id(file)
        if speaker_id:
            directory_speaker_count[directory_name].add(speaker_id)
            speaker_file_count[speaker_id] += 1


print("Unique Speakers Per Directory:")
for directory, speakers in directory_speaker_count.items():
    print(f"Directory '{directory}' has {len(speakers)} unique speakers")

print("\nVoice Files Per Speaker:")
for speaker, count in speaker_file_count.items():
    print(f"Speaker {speaker} has {count} voice files")