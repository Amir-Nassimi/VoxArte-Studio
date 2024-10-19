import argparse
from inaSpeechSegmenter import Segmenter


class Detector:
    def __init__(self):
        self.segment_obj = Segmenter()

    def predict(self, path):
        return self.segment_obj(path)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adrs", type=str, required=True, help="path to audio")

    args = parser.parse_args()

    result = Detector().predict(args.adrs)
    print(result)

if __name__ == "__main__":
    main()
