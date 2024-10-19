import os
import itertools
import argparse

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--inp", help="data directory separated by speaker")
args = parser.parse_args()

# Get a list of speakers and their corresponding files
speakers = os.listdir(args.inp)
all_files = []
for speaker in speakers:
    files = os.listdir(f'{args.inp}/{speaker}')
    for file in files:
        all_files.append((f'{args.inp}/{speaker}/{file}', speaker))  # Keep track of the speaker

# Create combinations of files
combs = list(itertools.combinations(all_files, 2))

# Create trial files for True and False values
with open('trial_true.txt', 'w') as fout_true, open('trial_false.txt', 'w') as fout_false:
    for couple in combs:
        file1, speaker1 = couple[0]
        file2, speaker2 = couple[1]
        
        if speaker1 == speaker2:
            line = f"{file1} {file2} True"
            fout_true.write(line + '\n')
        else:
            line = f"{file1} {file2} False"
            fout_false.write(line + '\n')

# Debugging print statements
print(f"Total combinations: {len(combs)}")
print(f"True pairs: {sum(1 for couple in combs if couple[0][1] == couple[1][1])}")
print(f"False pairs: {sum(1 for couple in combs if couple[0][1] != couple[1][1])}")