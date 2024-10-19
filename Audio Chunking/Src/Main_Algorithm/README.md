# Volume Analysis

This task is designed to split audios into desired chunks.

# Installation

Install dependencies via `requirements.txt`:
```shell script
pip install -r requirements.txt
```

# Usage
1. Import `AudioChunkProcessor` from utils:

```python
from audio_chunking.Src.utils.audio_chunk import AudioChunkProcessor
```

2. Run the followings:
```python
    audio_file = 'Path to audio file'

    audio = AudioSegment.from_file(audio_file)
    chunk = AudioChunkProcessor(chunk_duration_sec=1) #Duration of chunks in seconds
    chunk.process_chunks(audio)  

```

# Prediction

Run the ocr via the following command:
```shell script
    python test/test.py
```

# Output

the chunks will be saved in `.wav` format in Dataset dir.

# Metrics
1. Tiem = 0.06
2. Memory Usage = 62%
3. Acc = 100%