# Speech Recognition and Synthesis Project

This project is a Python application integrating both speech recognition and synthesis functionalities. It leverages advanced deep learning models and technologies to provide high-accuracy speech-to-text and text-to-speech services.

## Features

- Supports speech recognition in multiple languages, including Chinese, English, Cantonese, Japanese, Korean, and more.
- Uses an end-to-end speech recognition framework with fast recognition speed and low latency.
- Includes built-in emotion recognition and acoustic event detection capabilities, outputting rich-text transcriptions.
- Provides a convenient speech synthesis interface with customizable voice actors and speech styles.
- Complete service deployment solution, supporting multiple concurrent requests.

## Environment Setup

To run this project, you first need to set up a Python development environment. We recommend using Anaconda to manage Python environments and dependencies.

### Create a Conda Environment

First, make sure you have Anaconda or Miniconda installed. Then, open your terminal and run the following command to create a conda environment named `fish-speech`:

```
conda create -n fish-speech python=3.10
```

After the environment is created, activate it with:

```
conda activate fish-speech
```

Install `ffmpeg` in the environment:

```
conda install -c conda-forge ffmpeg
```

### Install Python Dependencies

The project relies on several third-party Python libraries. To install them, run:

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements-tts.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

The `requirements.txt` and `requirements-tts.txt` files list all required dependencies and their versions. We use Tsinghua University's PyPI mirror to speed up the installation process.

Specifically, for PyTorch installation, we recommend selecting the appropriate CUDA version based on your GPU model from the [PyTorch website](https://pytorch.org/get-started/locally/). The `requirements.txt` includes the CPU version of PyTorch. If you plan to use local speech models instead of online services, you need to install the GPU version of PyTorch.

### Configure Environment Variables

In the project root directory, there is a `.env` file used for configuring environment variables. Fill in the necessary information according to the comments, such as API keys, service addresses, etc.

## Usage Instructions

### Speech Recognition

To use the speech recognition feature, run the `asr_client.py` file:

```
python asr_client.py
```

The program will prompt you to enter an audio file path or URL. After inputting, the program will call the ModelScope speech recognition pipeline to transcribe the audio and print the results to the console.

You can also modify the `asr_client.py` code to adjust recognition parameters, such as language type and whether to output punctuation. For specific parameter details, please refer to the code comments.

### Speech Synthesis

To use the speech synthesis feature, run the `tts_client.py` file:

```
python tts_client.py
```

The program will prompt you to enter the text to be synthesized. After inputting, the program will call the ModelScope speech synthesis pipeline to convert the text into speech, play the synthesized audio, and save the audio file locally.

You can modify the `tts_client.py` code to customize synthesis parameters, such as voice actor, speech rate, volume, etc. For specific parameter details, please refer to the code comments.

### Using `websocat` with FastAPI

You can use the `websocat` command to request the FastAPI server. Here is an example of how to connect via WebSocket for speech recognition and synthesis:

1. Start the FastAPI server:

```
python server.py --port 27000
```

2. Use the `websocat` command to connect to the WebSocket endpoint and send audio data:

```
websocat ws://localhost:27000/ws/transcribe < path_to_your_audio_file.wav
```

Replace `path_to_your_audio_file.wav` with the path to the audio file you want to send.

## References

- [ModelScope Official Documentation](https://www.modelscope.cn/docs)  
- [FunASR Speech Recognition Toolkit](https://github.com/alibaba-damo-academy/FunASR)

## Feedback

If you encounter any issues while using the project, please submit an issue on GitHub, and we will respond as soon as possible. If you have any suggestions for improvements or new feature requests, feel free to submit a PR to contribute code.

We hope this project helps with your work and learning! If you have any questions, please feel free to contact us.