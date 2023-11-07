import os
import argparse
import soundfile as sf
from pedalboard import *
from pedalboard.io import AudioFile
from pedalboard import Pedalboard, Compressor, Gain, PitchShift,Mix
import ffmpeg
import pathlib

class Pitch_shift:
    '''
    arguments:
    sample_rate: desired sample rate
    '''

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def streo_to_mono(self, input_audio, preprocessed_audio):
        '''
        Produces a mono audio file
        Inputs:
        input_audio: The audio file uploaded by the user.
        preprocessed_audio: Audio file changed from stereo to mono.
        '''

        os.system(f"ffmpeg -y -i {input_audio} -ac 1 {preprocessed_audio}")

    def resample_and_load(self, preprocessed_audio):
        '''
        It changes the sampling rate of the audio file to the desired rate and loads the audio file
        inputs:
        preprocessed_audio: Audio file changed from stereo to mono.
        outputs:
        loaded_audio: The audio file whose sampling rate has been changed and loaded.
        '''

        with AudioFile(preprocessed_audio).resampled_to(self.sample_rate) as f:
            loaded_audio = f.read(f.frames)
        return loaded_audio

    def define_pitchshift_board(self, pitchshift_step):
        '''
        this function defines a padelboard to do pitch shift.
        Inputs:
        pitchshift_step: Number of pitch shift steps
        outputs:
        pitchshift_board: defined pedalboard
        '''

        pitch_shift = Pedalboard([PitchShift(semitones=pitchshift_step), Gain(gain_db=0)])
        pitchshift_board = Pedalboard([Compressor(), Mix([pitch_shift])])
        return pitchshift_board

    def separate_audio_parts(self, loaded_audio, start_sec, end_sec):
        '''
        Converts the audio file into two parts. The part that needs to be pitchshifted and a list of parts that are not to be changed.
        Inputs:
        loaded_audio: loaded audio file
        start_sec: Time to start applying pitch shift
        end_sec: Time to end applying pitch shift
        outputs:
        interest_audio_part: The part that needs to be pitchshifted
        not_interest_audio_part: list of parts that are not to be changed
        '''

        if not end_sec:
            end_sec = len(loaded_audio[0])
        start_smpl = int(start_sec*self.sample_rate)
        end_smpl = int(end_sec*self.sample_rate)
        interest_audio_part = loaded_audio[0][start_smpl:end_smpl]
        audiofile_beginning_part = loaded_audio[0][:start_smpl].tolist()
        audiofile_end_part = loaded_audio[0][end_smpl:].tolist()
        not_interest_audio_parts = [audiofile_beginning_part, audiofile_end_part]
        return interest_audio_part, not_interest_audio_parts

    def pitch_shift(self, pitchshift_board, interest_audio_part):
        '''
        Apply pitch shift to the desired part
        Inputs:
        pitchshift_board: defined pedalboard
        interest_audio_part: The part that needs to be pitchshifted
        outputs:
        effected_interest_audio_part: pitchshifted part of audio
        '''

        effected_interest_audio_part = pitchshift_board(interest_audio_part.reshape(1,interest_audio_part.shape[0]), self.sample_rate)[0].tolist()
        return effected_interest_audio_part

    def generate_processed_audio(self, effected_interest_audio_part, not_interest_audio_parts, output_path):
        '''
        Producing and writing the final audio file
        Inputs:
        effected_interest_audio_part: pitchshifted part of audio
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
    parser.add_argument("--step", type=int, default=1, help="step from -5 to 10")
    args = parser.parse_args()

    pathlib.Path(args.temp).mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    pitch_shift = Pitch_shift()

    name = os.path.splitext(os.path.basename(args.input))[0]
    preprocessed_audio = f'{args.temp}/{name}.wav'
    pitch_shift.streo_to_mono(args.input, preprocessed_audio)
    loaded_audio = pitch_shift.resample_and_load(preprocessed_audio)
    pitchshift_board = pitch_shift.define_pitchshift_board(args.step)
    interest_audio_part, not_interest_audio_parts = pitch_shift.separate_audio_parts(loaded_audio, args.start, args.end)
    effected_interest_audio_part = pitch_shift.pitch_shift(pitchshift_board, interest_audio_part)
    output_path = f'{args.out}/step{args.step}_{name}.wav'
    pitch_shift.generate_processed_audio(effected_interest_audio_part, not_interest_audio_parts, output_path)
    pitch_shift.clean_temp_dir(preprocessed_audio)
    final_information = pitch_shift.give_information(output_path)

if __name__=="__main__":
    main()
