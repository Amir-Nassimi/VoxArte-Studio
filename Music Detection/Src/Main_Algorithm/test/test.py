import psutil
import os, sys
from time import time
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__).resolve().parents[2]))
from utils.music_detector import Music_Detection


def main():
    audio_file = f'{os.path.abspath(Path(__file__).resolve().parents[3])}/Dataset/Zan.wav'
    detector = Music_Detection()

    t = time()
    detector.analyze(audio_file)
    z = time() - t

    print(f'Time: {z}')
    print(f'Memory: {psutil.virtual_memory().percent}')

if __name__ == "__main__":
    main()
