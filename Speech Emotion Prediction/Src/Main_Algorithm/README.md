# Speech Emotion

Speech emotion recognition (SER) is the process of predicting human emotions from audio signals using artificial intelligence (AI) techniques. SER technologies have a wide range of applications in areas such as psychology, medicine, education, and entertainment.

# Installation

follow this command in `python 3.10.13` environment:

```bash
pip install -r requirements.txt
```

# Testing

```bash
python speech_emotion_prediction/Src/Main_Algorithm/Code/detector.py --adrs
```
`adrs`: path to audio file

# Prediction

feel free to use the following commands as well:

## Usage

```python
from Code.detector import Detector

path = 'speech_emotion_prediction/Dataset/Mard.wav'

results = Detector().predict(path)
```

## Output

```python
[{'Label': 'Anger', 'Score': '0.0%'},
 {'Label': 'Fear', 'Score': '0.0%'},
 {'Label': 'Happiness', 'Score': '0.0%'},
 {'Label': 'Neutral', 'Score': '99.8%'},
 {'Label': 'Sadness', 'Score': '0.1%'},
 {'Label': 'Surprise', 'Score': '0.1%'}]
```