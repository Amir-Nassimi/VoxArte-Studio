import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__).resolve().parents[1]))
from Code.detector import Detector


result = Detector().predict(f'{os.path.abspath(Path(__file__).resolve().parents[3])}/Dataset/Zan.wav')
print(result)    