import argparse
import os

import librosa
import numpy as np
import soundfile as sf
from tqdm import tqdm

from lib.dataset import make_padding
from lib.nets import CascadedNet
from lib.spec_utils import wave_to_spectrogram, merge_artifacts, spectrogram_to_wave

import torch
import torchaudio

class Separator(object):
    '''
    This module isolates the sound related to the sound production sources. It saves the sounds produced by the human speech device in one file and the other sounds in a separate audio file
    Arguments:
    pre_model: pretrained spirce separator model
    hop_length: hop length for convertinf wav to spectrogram
    batchsize: batchsize to convert spectrogram into chunks
    postprocess: whether to postprocess or not
    n_fft: n_fft to define model
    gpu: use gpu
    '''

    def __init__(self, pre_model, hop_length, batchsize, cropsize, n_fft, gpu, postprocess=False):
        self.pre_model = pre_model
        self.hop_length = hop_length
        self.batchsize = batchsize
        self.cropsize = cropsize
        self.postprocess = postprocess
        self.n_fft = n_fft

        self.device = torch.device('cpu')
        self.model = CascadedNet(self.n_fft, 32, 128)
        self.model.load_state_dict(torch.load(self.pre_model, map_location=self.device))
        self.offset = self.model.offset

        if gpu >= 0:
            if torch.cuda.is_available():
                device = torch.device('cuda:{}'.format(gpu))
                self.model.to(device)
            elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
                device = torch.device('mps')
                self.model.to(device)

    def spect(self, input_audio, desired_sr):
        '''
        convert waveform to spectrogram
        Inputs:
        input_audio: input audio file path
        desired_sr: desired sample rate
        outputs:
        X_spec: spectrogram
        sr: audio sample rate
        '''
        X, sr = librosa.load(
            input_audio, sr=desired_sr, mono=False, dtype=np.float32, res_type='kaiser_fast')

        if X.ndim == 1:
            # mono to stereo
            X = np.asarray([X, X])

        X_spec = wave_to_spectrogram(X, self.hop_length, self.n_fft)
        return X_spec, sr

    def _separate(self, X_mag_pad, roi_size):
        '''
        Mask generation using the model to isolate sound sources
        '''
        X_dataset = []
        patches = (X_mag_pad.shape[2] - 2 * self.offset) // roi_size
        for i in range(patches):
            start = i * roi_size
            X_mag_crop = X_mag_pad[:, :, start:start + self.cropsize]
            X_dataset.append(X_mag_crop)

        X_dataset = np.asarray(X_dataset)

        self.model.eval()
        with torch.no_grad():
            mask = []
            # To reduce the overhead, dataloader is not used.
            for i in tqdm(range(0, patches, self.batchsize)):
                X_batch = X_dataset[i: i + self.batchsize]
                X_batch = torch.from_numpy(X_batch).to(self.device)

                pred = self.model.predict_mask(X_batch)

                pred = pred.detach().cpu().numpy()
                pred = np.concatenate(pred, axis=2)
                mask.append(pred)

            mask = np.concatenate(mask, axis=2)

        return mask

    def _preprocess(self, X_spec):
        '''
        Separation of spectrogram into amplitude and phase
        '''

        X_mag = np.abs(X_spec)
        X_phase = np.angle(X_spec)

        return X_mag, X_phase

    def _postprocess(self, mask, X_mag, X_phase):
        '''
        Isolation of sound sources
        '''

        if self.postprocess:
            mask = merge_artifacts(mask)

        y_spec = mask * X_mag * np.exp(1.j * X_phase)
        v_spec = (1 - mask) * X_mag * np.exp(1.j * X_phase)

        return y_spec, v_spec

    def separate(self, X_spec):
        '''
        Do preprocess and postprocess
        '''
        X_mag, X_phase = self._preprocess(X_spec)

        n_frame = X_mag.shape[2]
        pad_l, pad_r, roi_size = make_padding(n_frame, self.cropsize, self.offset)
        X_mag_pad = np.pad(X_mag, ((0, 0), (0, 0), (pad_l, pad_r)), mode='constant')
        X_mag_pad /= X_mag_pad.max()

        mask = self._separate(X_mag_pad, roi_size)
        mask = mask[:, :, :n_frame]

        y_spec, v_spec = self._postprocess(mask, X_mag, X_phase)

        return y_spec, v_spec

    def separate_tta(self, X_spec):
        X_mag, X_phase = self._preprocess(X_spec)

        n_frame = X_mag.shape[2]
        pad_l, pad_r, roi_size = make_padding(n_frame, self.cropsize, self.offset)
        X_mag_pad = np.pad(X_mag, ((0, 0), (0, 0), (pad_l, pad_r)), mode='constant')
        X_mag_pad /= X_mag_pad.max()

        mask = self._separate(X_mag_pad, roi_size)

        pad_l += roi_size // 2
        pad_r += roi_size // 2
        X_mag_pad = np.pad(X_mag, ((0, 0), (0, 0), (pad_l, pad_r)), mode='constant')
        X_mag_pad /= X_mag_pad.max()

        mask_tta = self._separate(X_mag_pad, roi_size)
        mask_tta = mask_tta[:, :, roi_size // 2:]
        mask = (mask[:, :, :n_frame] + mask_tta[:, :, :n_frame]) * 0.5

        y_spec, v_spec = self._postprocess(mask, X_mag, X_phase)

        return y_spec, v_spec

    def spec_to_wav(self, spec, output_file, sr):
        '''
        convertx spectrogram to wave
        '''
        wave = spectrogram_to_wave(spec, hop_length=self.hop_length)
        sf.write(output_file, wave.T, sr)

    def give_information(self, vocal_file, instrument_file, sr):
        '''
        Giving information about the final audio file
        '''
        information = {"vocal_file": vocal_file, "instrument_file": instrument_file, "output_sr": sr, "output_channels": 2 ,"output_format": "wav"}
        return information


def main():

    p = argparse.ArgumentParser()
    p.add_argument('--gpu', '-g', type=int, default=-1)
    p.add_argument('--pretrained_model', '-P', type=str, default='models/baseline.pth')
    p.add_argument('--input', '-i', required=True)
    p.add_argument('--sr', '-r', type=int, default=44100)
    p.add_argument('--n_fft', '-f', type=int, default=2048)
    p.add_argument('--hop_length', '-H', type=int, default=1024)
    p.add_argument('--batchsize', '-B', type=int, default=4)
    p.add_argument('--cropsize', '-c', type=int, default=256)
    p.add_argument('--postprocess', '-p', action='store_true')
    p.add_argument('--tta', '-t', action='store_true')
    p.add_argument('--out', '-o', type=str, default="")
    args = p.parse_args()

    basename = os.path.splitext(os.path.basename(args.input))[0]

    separator = Separator(args.pretrained_model, args.hop_length, args.batchsize, args.cropsize, args.n_fft, args.gpu, args.postprocess)
    X_spec, sr = separator.spect(args.input, args.sr)

    if args.tta:
        y_spec, v_spec = separator.separate_tta(X_spec)
    else:
        y_spec, v_spec = separator.separate(X_spec)

    if args.out != "":  # modifies output_dir if theres an arg specified
        output_dir = args.out.rstrip('/') + '/'
        os.makedirs(output_dir, exist_ok=True)

    vocal_file = '{}{}_Vocals.wav'.format(args.out, basename)
    separator.spec_to_wav(v_spec, vocal_file, sr)
    instrument_file = '{}{}_Instruments.wav'.format(args.out, basename)
    separator.spec_to_wav(y_spec, instrument_file, sr)

    final_information = separator.give_information(vocal_file, instrument_file, sr)

if __name__ == '__main__':
    main()
