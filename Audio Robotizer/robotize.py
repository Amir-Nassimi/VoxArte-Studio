import os
import argparse
import soundfile as sf
import ffmpeg
import torchaudio
import pathlib

class Robotize:
    '''
    arguments:
    sample_rate: desired sample rate
    '''

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def do_robotize(self, input_audio, processed_audio):
        '''
        Robotizes the entire audio file
        Inputs:
        input_audio:  The audio file uploaded by the user
        processed_audio: robotized audio file
        '''

        os.system(f'''ffmpeg -y -i {input_audio} -ar {self.sample_rate} -ac 1 -filter_complex "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75" {processed_audio}''')

    def load_audio_file(self, input_audio, processed_audio):
        '''
        The original audio file and the robotized audio file are loaded
        Inputs:
        input_audio:  The audio file uploaded by the user
        processed_audio: robotized audio file
        outputs:
        original_waveform: The original file that is loaded
        robotize_waveform: The robotized file that is loaded
        '''

        original_waveform, _ = torchaudio.load(input_audio, normalize=True)
        robotized_waveform, _ =  torchaudio.load(processed_audio, normalize=True)
        return original_waveform, robotized_waveform

    def generate_final_waveform(self, original_waveform, robotize_waveform, start_sec, end_sec):
        '''

        Inputs:
        original_waveform: The original file that is loaded
        robotize_waveform: The robotized file that is loaded
        start_sec: Time to start applying robotize
        end_sec: Time to end applying robotize
        outputs:
        final_waveform: final robotized waveform
        '''

        if not end_sec:
            end_sec = len(original_waveform[0])
        start_smpl = int(start_sec*self.sample_rate)
        end_smpl = int(end_sec*self.sample_rate)
        final_waveform = original_waveform[0][:start_smpl].tolist() + robotize_waveform[0][start_smpl:end_smpl].tolist() + original_waveform[0][end_smpl:].tolist()
        return final_waveform

    def replace_audio_content(self, final_waveform, robotized_audio):
        '''
        replacing robotized_audio content with final_waveform
        '''

        sf.write(robotized_audio, final_waveform, self.sample_rate)

    def give_information(self, output_path):
        '''
        Giving information about the final audio file
        Inputs:
        output_path: final audio file path
        '''

        information = {"output_file": output_path, "output_sr": self.sample_rate, "output_channels": 1 ,"output_format": "wav"}
        return information


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=str, help="Input audio file")
    parser.add_argument("--out", required=True, type=str, help="Output directory")
    parser.add_argument("--start", required=False, type=float or int, default=0, help="start time - second")
    parser.add_argument("--end", required=False, type=float or int, default=0, help="end time - second")
    args = parser.parse_args()

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    robotize = Robotize()

    name = os.path.splitext(os.path.basename(args.input))[0]
    robotized_audio = f'{args.out}/robot_{name}.wav'
    robotize.do_robotize(args.input, robotized_audio)

    if args.start or args.end:
        original_waveform, robotize_waveform = robotize.load_audio_file(args.input, robotized_audio)
        final_waveform = robotize.generate_final_waveform(original_waveform, robotize_waveform, args.start, args.end)
        robotize.replace_audio_content(final_waveform, robotized_audio)

    info = robotize.give_information(robotized_audio)


if __name__=="__main__":
    main()
