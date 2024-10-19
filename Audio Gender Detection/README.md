# Speech Gender Detecttion
Gender voice is considered one of the pivotal parts to be detected from a given voice, a task that involves certain complications. In order to distinguish gender from a voice signal, a set of techniques have been employed to determine relevant features to be utilized for building a model from a training set

# Installation
follow this command in `python 3.10.13` environment:

```bash
pip install -r requirements.txt
```

# Prediction

```bash
python speech_gender_prediction/Src/Main_Algorithm/detector.py --adrs
```

`adrs`: path to audio

# Usage

```python
from speech_gender_prediction.Src.Main_Algorithm.detector import Detector
path = 'Evaluation_Dataset/Zan.wav'
result = Detector().predict(path)
```

# Output
```bash
[('noEnergy', 0.0, 0.9), ('female', 0.9, 2.14)]
```