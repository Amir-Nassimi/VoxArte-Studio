import os
import librosa
import argparse
import soundfile as sf
import ffmpeg
import pathlib

class Speed:
    '''
    arguments:
    sample_rate: desired sample rate
    '''

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def change_sr_ch(self, input_audio, preprocessed_audio):
        '''
        This function changes the sampling rate and the number of channels of the audio file

        Inputs:
        input_audio: The audio file uploaded by the user
        preprocessed_audio: Audio file whose sampling rate and number of channels have been changed
        '''

        os.system(f"ffmpeg -y -i {input_audio} -ar {self.sample_rate} -ac 1 {preprocessed_audio}")

    def load(self, preprocessed_audio):
        '''
        Loads the audio file
        Inputs:
        preprocessed_audio: Audio file whose sampling rate and number of channels have been changed
        outputs:
        loaded_audio: Audio file loaded by librosa
        '''

        loaded_audio, _ = librosa.load(preprocessed_audio, sr=self.sample_rate)
        return loaded_audio

    def separate_audio_parts(self, loaded_audio, start_sec, end_sec):
        '''
        Converts the audio file into two parts. The part that needs to be speed changed and a list of parts that are not to be changed.
        Inputs:
        loaded_audio: loaded audio file
        start_sec: Time to start applying speed change
        end_sec: Time to end applying speed change
        outputs:
        interest_audio_part: The part that needs to be speed changed
        not_interest_audio_part: list of parts that are not to be changed
        '''

        if not end_sec:
            end_sec = len(loaded_audio)
        start_smpl = int(start_sec*self.sample_rate)
        end_smpl = int(end_sec*self.sample_rate)
        interest_audio_part = loaded_audio[start_smpl:end_smpl]
        audiofile_beginning_part = loaded_audio[:start_smpl].tolist()
        audiofile_end_part = loaded_audio[end_smpl:].tolist()
        not_interest_audio_parts = [audiofile_beginning_part, audiofile_end_part]
        return interest_audio_part, not_interest_audio_parts

    def speed_change(self, interest_audio_part, speed_rate):
        '''
        Apply speed change to the desired part
        Inputs:
        interest_audio_part: The part that needs to be speed changed
        outputs:
        effected_interest_audio_part: speed changed part of audio
        '''

        effected_interest_audio_part = librosa.effects.time_stretch(interest_audio_part, rate=speed_rate).tolist()
        return effected_interest_audio_part

    def generate_processed_audio(self, effected_interest_audio_part, not_interest_audio_parts, output_path):
        '''
        Producing and writing the final audio file
        Inputs:
        effected_interest_audio_part: speed changed part of audio
        not_interest_audio_parts: list of parts that are not to be changed
        output_path: final audio file path
        '''

        final_waveform = not_interest_audio_parts[0] + effected_interest_audio_part + not_interest_audio_parts[1]
        sf.write(output_path, final_waveform, self.sample_rate)

    def clean_temp_dir(self, processed_audio):
        '''
        Delete the audio files of the temp directory after processing
        '''

        os.remove(processed_audio)

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
    parser.add_argument("--temp", required=True, type=str, help="temp directory")
    parser.add_argument("--start", required=False, type=float or int, default=0, help="start time - second")
    parser.add_argument("--end", required=False, type=float or int, default=0, help="end time - second")
    parser.add_argument("--rate", type=float or int, default=1, help="select from 0.5 to 2")
    args = parser.parse_args()

    pathlib.Path(args.temp).mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    speed = Speed()

    name = os.path.splitext(os.path.basename(args.input))[0]
    preprocessed_audio = f'{args.temp}/{name}.wav'
    speed.change_sr_ch(args.input, preprocessed_audio)

    loaded_audio = speed.load(preprocessed_audio)
    interest_audio_part, not_interest_audio_parts = speed.separate_audio_parts(loaded_audio, args.start, args.end)
    effected_interest_audio_part = speed.speed_change(interest_audio_part, args.rate)
    output_path = f'{args.out}/rate_{args.rate}_{name}.wav'
    speed.generate_processed_audio(effected_interest_audio_part, not_interest_audio_parts, output_path)
    speed.clean_temp_dir(preprocessed_audio)
    final_information = speed.give_information(output_path)

if __name__=="__main__":
    main()
