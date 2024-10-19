from pydub import AudioSegment

import psutil
import os, sys
from time import time
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__).resolve().parents[2]))
from utils.audio_chunk import AudioChunkProcessor


def main():
    audio_file = f'{os.path.abspath(Path(__file__).resolve().parents[3])}/Dataset/Zan.wav'
    audio = AudioSegment.from_file(audio_file)

    chunk = AudioChunkProcessor(chunk_duration_sec=1)

    t = time()
    chunk.process_chunks(audio) 
    z = time() - t

    print(f'Time: {z}')
    print(f'Memory: {psutil.virtual_memory().percent}')

if __name__ == "__main__":
    main()
