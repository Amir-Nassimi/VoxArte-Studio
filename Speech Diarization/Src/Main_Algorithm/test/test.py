import psutil
import os, sys
from time import time
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__).resolve().parents[2]))
from utils.diarization import SpeakerDiarization


def main():
    audio_file = f'{os.path.abspath(Path(__file__).resolve().parents[3])}/Dataset/Zan.wav'
    diarizer = SpeakerDiarization("pyannote/speaker-diarization-3.1", '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')

    t = time()
    results = diarizer.process_audio(audio_file)
    z = time() - t

    # Output the results
    print("\n\n\nDiarization Results:")
    for result in results:
        print(f"start: {result['start']:.1f}s, stop: {result['stop']:.1f}s, Speaker: {result['speaker']}")


    print(f'\n\nTime: {z}')
    print(f'Memory: {psutil.virtual_memory().percent}')

if __name__ == "__main__":
    main()
