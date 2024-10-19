# Volume Analysis

This task is designed to measure the Average Volume (dBFS) of any given audio file using `pydub` library.

# Installation

Install dependencies via `requirements.txt`:
```shell script
pip install -r volume_analysis/Src/Main_Algorithm/requirements.txt
```

# Usage
1. Import `VoiceVolumeAnalyzer` from utils:

```python
from volume_analysis.Src.utils.volume_analysis import VoiceVolumeAnalyzer
```

2. Run the followings:
```python
    audio_file = 'Path to audio file'
    volume_detector = VoiceVolumeAnalyzer()
    audio = AudioSegment.from_file(audio_file)
    volume_out = volume_detector.analyze(audio) 
    print(f"Average Volume (dBFS): {volume_out}")
```

# Prediction

Run the ocr via the following command:
```shell script
    python volume_analysis/Src/Main_Algorithm/test/test.py
```

# Output

the output is a string:
`Average Volume (dBFS): -16.371391265539113

# Metrics
1. Tiem = 0
2. Memory Usage = 68%
3. Acc = 100%