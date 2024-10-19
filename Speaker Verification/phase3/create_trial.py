import os
import random
import re
import argparse
from collections import defaultdict

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--inp", help="Data directory containing sound files", required=True)
parser.add_argument("--num_other_speakers", type=int, default=4, help="Number of other speakers to compare against")
parser.add_argument("--num_trials", type=int, default=50000, help="Total number of trials to generate")
parser.add_argument("--output", default='new_trials_with_flags_new.txt', help="Output file name for generated trials")
parser.add_argument("--full_length", action='store_true', help="Use all audios for trials without skipping any")
args = parser.parse_args()

# Function to extract speaker ID from the filename
def extract_speaker_id(filename):
    match = re.match(r'^(\d+)-', filename)  # Extracts the number before the dash
    if match:
        return match.group(1)  # Return the number part as the speaker ID
    return None

# Gather all files and organize them by speaker
speaker_files = defaultdict(list)
for root, _, files in os.walk(args.inp):
    for file in files:
        speaker_id = extract_speaker_id(file)
        if speaker_id:
            full_path = os.path.join(root, file)
            speaker_files[speaker_id].append(full_path)

# Initialize counters for same and non-same speaker trials
same_speaker_count = 0
non_same_speaker_count = 0
trial_count = 0

with open(args.output, 'w') as f_out:
    while trial_count < args.num_trials:
        # Randomly decide if the next trial should be same speaker or not
        include_same_speaker = True if same_speaker_count < (args.num_trials // 2) else False

        # Step 1: Choose a base audio
        valid_speakers = {spk: files for spk, files in speaker_files.items() if len(files) >= 2}
        
        if not valid_speakers:
            break  # Exit if there are no valid speakers

        speaker_id, files = random.choice(list(valid_speakers.items()))
        base_audio = random.choice(files)

        # Step 2: Choose a same-speaker pair if applicable
        comparison_audios = []
        same_speaker_flag = 'False'

        if include_same_speaker:
            same_speaker_files = [f for f in files if f != base_audio]
            if same_speaker_files:
                same_speaker_audio = random.choice(same_speaker_files)
                comparison_audios.append(same_speaker_audio)
                same_speaker_flag = 'True'
                same_speaker_count += 1
            else:
                continue  # No valid same-speaker audio available, skip this trial

        # Step 3: Choose audios from other speakers
        other_speakers = list(set(speaker_files.keys()) - {speaker_id})
        if len(other_speakers) < args.num_other_speakers:
            continue  # Skip if not enough other speakers are available

        for other_speaker in random.sample(other_speakers, min(args.num_other_speakers, len(other_speakers))):
            other_audio = random.choice(speaker_files[other_speaker])
            comparison_audios.append(other_audio)

        # Step 4: Write the trial to the output file
        trial_line = f"{base_audio} " + " ".join(comparison_audios) + f" {same_speaker_flag}"
        f_out.write(trial_line + '\n')
        trial_count += 1

print(f"Trial file '{args.output}' generated successfully.")
