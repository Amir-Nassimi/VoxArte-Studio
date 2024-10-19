# Music Detection
This task is designed to detect music from audio in a file.

# Installation
1. Install pytorch utilizing the following command:
```shell script
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

2. Install dependencies via `requirements.txt`:
```shell script
pip install -r requirements.txt
```

# Usage
1. Import `Music_Detection` from utils:

```python
from music_detection.Src.utils.music_detector import Music_Detection
```

2. Run the followings:
```python
    audio_file = 'Path to audio file'

    detector = Music_Detection()
    detector.analyze(audio_file)

```

# Prediction
Run the ocr via the following command:
```shell script
    python test/test.py
```

# Output
the information will be printed:
```shell
00:05:47 Music (1.000)                                                                                                 
00:05:48 Music (1.000)                                                                                                 
00:05:49 Music (1.000)                                                                                                 
00:05:50 Music (1.000)                                                                                                 
00:05:51 Speech (1.000)                                                                                                 
00:05:52 Speech (1.000)                                                                                                 
00:05:53 Speech (1.000)                                                                                                 
00:05:54 Speech (1.000)
```

# Metrics
for a 5 minute audio file:
    1. Tiem = 2.20
    2. Memory Usage = 75%
    3. Acc = 100%