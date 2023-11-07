# VoxArte Studio

Welcome to VoxArte Studio – the quintessential suite for transforming your auditory experience with pitch shifting, voice speed modulation, robotization effects, and now, advanced audio denoising.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Build and Test](#build-and-test)
- [Audio Denoising](#audio-denoising)
- [Valid Formats](#valid-formats)
- [Explore Our Kernel 🚀](#explore-our-kernel-)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)
- [Credits and Acknowledgements](#credits-and-acknowledgements)
- [License](#license)
- [Contact Information](#contact-information)

## Introduction
VoxArte Studio now offers a comprehensive auditory suite with the addition of two innovative denoising options. By leveraging powerful audio processing libraries, VoxArte Studio enables real-time and offline pitch shifting, voice speed modulation, robotization effects, and advanced noise reduction capabilities.

## Features
- **Audio Pitch Shift**: Real-time and offline processing, configurable pitch range, and command-line interface. can be accessed in ***Audio Pitch Shift*** directory.
- **Audio Speed Changer**: Adjustable speed without affecting pitch, real-time modifications, and batch processing.can be accessed in ***Audio Speed Changer*** directory.
- **Robotize Effect**: Customizable robotic timbre, real-time effect application, and digital pedalboard effects.can be accessed in ***Robotizer*** directory.
- **High Noise Removal**: Powerful denoising that may affect the speaker's voice but removes significant background noise.can be accessed in ***Denoisers*** directory.
- **Low Noise Removal**: A gentler denoising process that preserves the speaker's voice quality while removing background noise.can be accessed in ***Denoisers*** directory.
Both of ***Noise Removal*** methods can be used in real-time processing, allowing for noise reduction without latency, perfect for live applications.

## Installation
To get started with VoxArte Studio, ensure you have FFmpeg installed:

```bash
sudo apt install ffmpeg
pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cpu
```

Then, clone the repository and install the Python dependencies:

```bash
git clone https://github.com/Amir-Nassimi/VoxArte-Studio.git
cd VoxArte-Studio
pip install -r requirements.txt #Exists in each directory
```

## Build and Test
Transform your audio files with these commands:

### Pitch Shift
```bash
python pitch_shift.py  --input [input audio file] --out [output directory] --temp [temp directory] --step [from -5 to 10] --start [optional - second] --end [optional - second] --format [optional - from format list]
```

### Robotize
```bash
python robotize.py --input  [input audio file] --out [output directory] --start [optional - second] --end [optional - second] --format [optional - from format list]
```

### Speed Change
```bash
python speed.py --input  [input audio file] --out [output directory] --temp [temp directory] --rate [from 0.5 to 2] --start [optional - second] --end [optional - second] --format [optional - from format list]
```

### Noise Removal
Please Download the [Weight](https://drive.google.com/file/d/1L4exxzsACOx2cqA2AWdv6d77QnUM0E5s/view?usp=sharing) from following link and put it inside the VoxArte-Studio/Audio Denoisers/models dir

#### High Noise Removal
```bash
python3 high_denoise.py --input [input audio file] --out [output directory] --temp [temp directory] --format [output audio format]
```

#### Low Noise Removal
```bash
python3 low_denoise.py --input [input audio file] --out [output directory] --format [output audio format]
```

## Valid Formats
VoxArte Studio supports a variety of audio formats, including:
- ogg
- flac
- mp3
- aiff
- aac
- m4a

# Explore Our Kernel 🚀
We are thrilled to unveil our cutting-edge kernel, an embodiment of innovation that integrates the audio manipulation capabilities of VoxArte Studio! It's not just a repository; it's a revolution in audio processing, built with our audio projects at its heart.

## Catch the Wave of Audio Innovation
Don't miss out on this opportunity to be a part of the audio evolution. Click the link blow, star the repo for future updates, and let your ears be the judge. If you're as passionate about audio as we are, we look forward to seeing you there!

Remember, the future of audio is not just heard; it's shared and shaped by enthusiasts and professionals alike. Let's make waves together with VoxArte Studio and our Kernel. 🚀

🔗 [Kernel Repository](https://github.com/Meta-Intelligence-Services)

---

For any queries or discussions regarding our kernel, feel free to open an issue in the kernel's repository, and we'll be more than happy to engage with you. Together, we're not just changing audio; we're making history!

## Technology Stack
VoxArte Studio harnesses a collection of powerful libraries and frameworks to provide its audio processing capabilities:

- **FFmpeg**: A complete, cross-platform solution to record, convert and stream audio and video.
- **Librosa**: A Python package for music and audio analysis, providing the building blocks necessary to create music information retrieval systems.
- **Soundfile**: A library for reading from and writing to a wide range of audio file formats.
- **Torch**: An open-source machine learning library, a scientific computing framework, and a script language based on the Lua programming language.
- **Torchvision**: A package consisting of popular datasets, model architectures, and common image transformations for computer vision.
- **Torchaudio**: Provides easy access to audio processing in PyTorch.
- **Denoiser**: Likely refers to a specific library or tool for removing noise from audio tracks.
- **TQDM**: A fast, extensible progress bar for Python and CLI that can be added to your code in seconds.
- **OpenCV-Python (opencv_python)**: A library of Python bindings designed to solve computer vision problems.
- **Resampy**: A Python module for high-quality audio resampling.

Make sure to install all required libraries using the `requirements.txt` file - which exists in each project's directory - or manually install them with `pip` if necessary.


## Contributing
While we deeply value community input and interest in VoxArte Studio, the project is currently in a phase where we're mapping out our next steps and are not accepting contributions just yet. We are incredibly grateful for your support and understanding. Please stay tuned for future updates when we'll be ready to welcome contributions with open arms.

## Credits and Acknowledgements
We would like to extend our heartfelt thanks to Mrs.Arefe Khaleghi for her guidance and wisdom throughout the development of VoxArte Studio. Her insights have been a beacon of inspiration for this project.

## License
VoxArte Studio is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

## Contact Information
Although we're not open to contributions at the moment, your feedback and support are always welcome. Please feel free to star the project or share your thoughts through the Issues tab on GitHub, and we promise to consider them carefully.