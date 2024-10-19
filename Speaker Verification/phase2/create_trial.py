import os
import itertools
import argparse
import re
import random

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--inp", help="data directory containing sound files")
parser.add_argument("--min_true", type=int, default=25000, help="Minimum number of True pairs")
parser.add_argument("--min_false", type=int, default=55000, help="Minimum number of False pairs")
args = parser.parse_args()

# Function to extract speaker ID from the filename
def extract_speaker_id(filename):
    match = re.match(r'^(\d+)-', filename)
    if match:
        return match.group(1)  # Return the number part as the speaker ID
    return None

# Traverse all directories and gather all files based on speaker ID
speaker_files = {}  # Dictionary to store files by speaker ID

for root, _, files in os.walk(args.inp):
    for file in files:
        speaker_id = extract_speaker_id(file)
        if speaker_id:
            # Store the full path of the file under the speaker ID
            if speaker_id not in speaker_files:
                speaker_files[speaker_id] = []
            speaker_files[speaker_id].append(os.path.join(root, file))

# Create True and False combinations
true_combs = set()  # Use a set to prevent duplicates
false_combs = set()  # Use a set to prevent duplicates

# Generate True pairs (same speaker ID)
for speaker_id, files in speaker_files.items():
    for file1, file2 in itertools.combinations(files, 2):
        true_combs.add((file1, file2))  # Store as a tuple to ensure uniqueness

# Generate False pairs (different speaker IDs)
speaker_ids = list(speaker_files.keys())
for comb in itertools.combinations(speaker_ids, 2):  # Pairing different speaker IDs
    files1 = speaker_files[comb[0]]
    files2 = speaker_files[comb[1]]
    for file1, file2 in itertools.product(files1, files2):
        false_combs.add((file1, file2))  # Store as a tuple to ensure uniqueness

# Ensure we meet the minimum number of True and False pairs
if len(true_combs) < args.min_true:
    raise ValueError(f"Not enough True pairs available. Only found {len(true_combs)} pairs.")
if len(false_combs) < args.min_false:
    raise ValueError(f"Not enough False pairs available. Only found {len(false_combs)} pairs.")

# Convert sets to lists before sampling
selected_true_combs = random.sample(list(true_combs), args.min_true)
selected_false_combs = random.sample(list(false_combs), args.min_false)

# Write the selected pairs to files
with open('trial_true.txt', 'w') as fout_true, open('trial_false.txt', 'w') as fout_false:
    for couple in selected_true_combs:
        file1, file2 = couple
        line = f"{file1} {file2} True"
        fout_true.write(line + '\n')

    for couple in selected_false_combs:
        file1, file2 = couple
        line = f"{file1} {file2} False"
        fout_false.write(line + '\n')

# Debugging print statements
print(f"Total True pairs generated: {len(selected_true_combs)}")
print(f"Total False pairs generated: {len(selected_false_combs)}")