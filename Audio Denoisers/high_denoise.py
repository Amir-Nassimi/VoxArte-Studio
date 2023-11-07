import argparse
import os
import soundfile as sf
import pathlib

import torch
import torchaudio
from denoiser import pretrained
from denoiser.dsp import convert_audio

class Denoiser:
    '''
    Arguments:
    model: pretrained denoising model
    '''

    def __init__(self, temp_dir, model=pretrained.dns64()):
        self.temp_dir = temp_dir
        self.model = model

    def change_sr(self, input_audio, preprocessed_audio):
        '''
        This function changes the sampling rate of the audio file

        Inputs:
        input_audio: The audio file uploaded by the user
        preprocessed_audio: Audio file whose sampling rate have been changed
        '''

        os.system(f"ffmpeg -y -i {input_audio} -ar {self.model.sample_rate} {preprocessed_audio}")


    def load(self, preprocessed_audio):
        '''
        Loads the audio file
        Inputs:
        preprocessed_audio: Audio file whose sampling rate have been changed
        outputs:
        loaded_audio: Audio file loaded by torchaudio
        audio_sr: Sampling rate of audo file
        '''

        loaded_audio, audio_sr = torchaudio.load(preprocessed_audio)
        return loaded_audio, audio_sr

    def convert_audio(self, loaded_audio, audio_sr):
        '''
        Convert the audio so that it is acceptable for the model
        Inputs:
        loaded_audio: Audio file loaded by torchaudio
        audio_sr: Sampling rate of audio file
        outputs:
        converted_audio: Acceptable audio file for the model
        '''

        converted_audio = convert_audio(loaded_audio, audio_sr, self.model.sample_rate, self.model.chin)
        return converted_audio

    def denoise(self, converted_audio, audio_sr, name):
        '''
        The audio file is converted into 30 second chunks. Each chunk is denoised and written as an audio file.
        Inputs:
        converted_audio: Acceptable audio file for the model
        audio_sr: Sampling rate of audio file
        name: name of input audio file
        outputs:
        denoised_chunks: List of denoised audio files, each corresponding to a 30-second chunk of data
        '''

        denoised_chunks = []
        count=0
        with torch.no_grad():
            st = 0
            end = int(audio_sr)*30
            while st<len(converted_audio[0]):
                count+=1
                actual_end = min(end, len(converted_audio[0]))
                denoised_audio = self.model(torch.tensor([converted_audio[0][st:actual_end].tolist()]))[0][0]
                st=end
                end+=int(audio_sr)*30
                sf.write(f"{self.temp_dir}/{name}-{count}.wav", denoised_audio, audio_sr)
                denoised_chunks.append(f"{self.temp_dir}/{name}-{count}.wav")
        return denoised_chunks

    def concatenate_chunks(self, denoised_chunks, output_path):
        '''
        concatenates audio files related to consecutive chunks with each other
        Inputs:
        denoised_chunks: List of denoised audio files, each corresponding to a 30-second chunk of data
        output_path: final audio file path
        '''

        command = "concat:"
        for denoised_chunk in denoised_chunks:
            command+=denoised_chunk
            command+='|'
        os.system(f"ffmpeg -y -i '{command}' {output_path}")


    def clean_temp_dir(self, preprocessed_audio, denoised_chunks):
        '''
        Delete the audio files of the temp directory after processing
        '''

        os.remove(preprocessed_audio)
        for denoised_chunk in denoised_chunks:
            os.remove(denoised_chunk)

    def give_information(self, output_path):
        '''
        Giving information about the final audio file
        Inputs:
        output_path: final audio file path
        '''

        information = {"output_file": output_path, "output_sr": self.model.sample_rate, "output_channels": 1 ,"output_format": "wav"}
        return information


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', '-i', required=True)
    p.add_argument('--out', '-o', type=str, default="")
    p.add_argument('--temp', '-t', type=str, default="")
    args = p.parse_args()

    pathlib.Path(args.temp).mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)

    denoiser = Denoiser(args.temp)

    name = os.path.split(args.input)[-1][:-4]
    if name[-1]==".":
        name = name[:-1]
    preprocessed_audio = f'{args.temp}/{name}.wav'
    denoiser.change_sr(args.input, preprocessed_audio)
    loaded_audio, audio_sr = denoiser.load(preprocessed_audio)
    converted_audio = denoiser.convert_audio(loaded_audio, audio_sr)
    denoised_chunks = denoiser.denoise(converted_audio, audio_sr, name)
    output_path =f'{args.out}/denoise_{name}.wav'
    denoiser.concatenate_chunks(denoised_chunks, output_path)
    denoiser.clean_temp_dir(preprocessed_audio, denoised_chunks)
    final_information = denoiser.give_information(output_path)


if __name__ == '__main__':
    main()
