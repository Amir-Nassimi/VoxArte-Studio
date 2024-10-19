import torch
import torch.nn.functional as F

import argparse
import torchaudio
from transformers import AutoConfig, Wav2Vec2FeatureExtractor

import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(__file__).resolve().parents[2]))

from utils.models import Wav2Vec2ForSpeechClassification


class Detector:
    def __init__(self, model_name = 'm3hrdadfi/wav2vec2-xlsr-persian-speech-emotion-recognition'):
        self.config = AutoConfig.from_pretrained(model_name)
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
        self.sampling_rate = self.feature_extractor.sampling_rate
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = Wav2Vec2ForSpeechClassification.from_pretrained(model_name).to(self.device)
    
    def speech_file_to_array_fm(self, path, sampling_rate):
        speech_array, _sampling_rate = torchaudio.load(path)
        resampler = torchaudio.transforms.Resample(_sampling_rate)
        speech = resampler(speech_array).squeeze().numpy()
        return speech

    def predict(self, path):
        speech = self.speech_file_to_array_fm(path, self.sampling_rate)
        inputs = self.feature_extractor(speech, sampling_rate=self.sampling_rate, return_tensors='pt', padding=True)
        inputs = {key:inputs[key].to(self.device) for key in inputs}

        with torch.no_grad():
            logits = self.model(**inputs).logits

        scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
        outputs = [{"Label": self.config.id2label[i], "Score":f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
        return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adrs", type=str, required=True, help="path to audio")

    args = parser.parse_args()

    result = Detector().predict(args.adrs)
    print(result)


if __name__ == "__main__":
    main()

    