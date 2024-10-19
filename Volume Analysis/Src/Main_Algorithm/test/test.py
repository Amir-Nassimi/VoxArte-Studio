from pydub import AudioSegment

import os, sys
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__).resolve().parents[2]))
from utils.volume_analysis import VoiceVolumeAnalyzer


def main():
    audio_file = f'{os.path.abspath(Path(__file__).resolve().parents[3])}/Dataset/Zan.wav'
    volume_detector = VoiceVolumeAnalyzer()
    audio = AudioSegment.from_file(audio_file)
    volume_out = volume_detector.analyze(audio) 
    print(f"Average Volume (dBFS): {volume_out}")


if __name__ == "__main__":
    main()
