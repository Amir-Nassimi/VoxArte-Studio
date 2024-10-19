# Speech Diarization

This task is designed to diarize the difference between multiple speakers.

# Installation

Install dependencies via `requirements.txt`:
```shell script
pip install -r requirements.txt
```

# Usage
1. Import `VoiceVolumeAnalyzer` from utils:

```python
from utils.diarization import SpeakerDiarization
```

2. Run the followings:
```python
    audio_file = 'Path to audio file'
    diarizer = SpeakerDiarization("pyannote/speaker-diarization-3.1", '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')
    results = diarizer.process_audio(audio_file)
```

3. Print the Results:
```python
    print("Diarization Results:")
    for result in results:
        print(f"start: {result['start']:.1f}s, stop: {result['stop']:.1f}s, Speaker: {result['speaker']}")
```

# Prediction

Run the ocr via the following command:
```shell script
    python test/test.py
```

# Output

the output is a string:
```python
Diarization Results:                                                                                                    
"start: 0.8s, stop: 2.1s, Speaker: speaker_SPEAKER_00"
```

# Metrics
1. Time = 0.62
2. Memory Usage = 76.8%
3. Acc = 100%