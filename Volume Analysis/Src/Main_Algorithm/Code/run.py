from pydub import AudioSegment

import psutil
import os, sys
from time import time
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__).resolve().parents[2]))
from utils.volume_analysis import VoiceVolumeAnalyzer


def main():
    audio_file = f'{os.path.abspath(Path(__file__).resolve().parents[3])}/Dataset/Zan.wav'
    volume_detector = VoiceVolumeAnalyzer()
    audio = AudioSegment.from_file(audio_file)
    t = time()
    volume_out = volume_detector.analyze(audio) 
    z = time() - t
    print(f"Average Volume (dBFS): {volume_out}")

    print(f'Time: {z}')
    print(f'Memory: {psutil.virtual_memory().percent}')

if __name__ == "__main__":
    main()
