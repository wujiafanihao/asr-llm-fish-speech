# 语音识别与语音合成项目

本项目是一个集成了语音识别与语音合成功能的Python应用程序。它利用了先进的深度学习模型和技术,提供了高精度的语音转文本和文本转语音服务。

## 功能特点

- 支持多种语言的语音识别,包括中文、英语、粤语、日语、韩语等
- 采用端到端的语音识别框架,识别速度快,延迟低 
- 内置情感识别和声学事件检测能力,可输出富文本转写结果
- 提供便捷的语音合成接口,可定制发音人和语音风格
- 完整的服务化部署方案,支持多并发请求

## 环境安装

为了运行本项目,您需要先配置好Python开发环境。我们推荐使用Anaconda来管理Python环境和依赖包。

### 创建conda环境

首先,确保您已经安装了Anaconda或Miniconda。然后,打开终端,运行以下命令创建一个名为`fish-speech`的conda环境:

```
conda create -n fish-speech python=3.10
```

创建完成后,激活该环境:

```
conda activate fish-speech
```

在环境中安装ffmpeg:

```
conda install -c conda-forge ffmpeg
```

### 安装Python依赖包

本项目依赖了一些第三方Python库。为了安装它们,请运行:

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements-tts.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

其中`requirements.txt`和`requirements-tts.txt`文件中列出了所有需要安装的依赖包及其版本号。我们使用了清华大学的PyPI镜像源以加速安装过程。

特别地,对于PyTorch的安装,我们建议您根据自己的GPU型号,到[PyTorch官网](https://pytorch.org/get-started/locally/)选择合适的CUDA版本进行安装。`requirements.txt`中提供的是CPU版本的PyTorch,如果您要使用本地的语音模型而不是在线服务,则需要安装GPU版本的PyTorch。

### 配置环境变量

在项目根目录下,有一个`.env`文件,用于配置一些环境变量。请根据注释说明,填写相应的配置信息,例如API密钥、服务地址等。

## 使用说明

### 语音识别

要使用语音识别功能,您可以运行`asr_client.py`文件:

```
python asr_client.py
```

程序会提示您输入一个音频文件路径或URL。输入后,程序会调用ModelScope的语音识别pipeline对音频进行转写,并将识别结果打印到控制台。

您还可以修改`asr_client.py`中的代码,调整识别参数,例如语言类型、是否输出标点符号等。具体参数说明请参考代码注释。

### 语音合成

要使用语音合成功能,您可以运行`tts_client.py`文件:

```
python tts_client.py
```

程序会提示您输入要合成的文本。输入后,程序会调用ModelScope的语音合成pipeline将文本转换为语音,并播放合成的音频。合成的音频文件也会保存到本地。

您可以修改`tts_client.py`中的代码来定制合成参数,例如发音人、语速、音量等。具体参数说明请参考代码注释。

### 使用`websocat`请求FastAPI

您可以使用`websocat`命令来请求FastAPI服务器。以下是一个示例，展示了如何通过WebSocket连接进行语音识别和合成：

1. 启动FastAPI服务器：

```
python server.py --port 27000
```

2. 使用`websocat`命令连接到WebSocket端点并发送音频数据：

```
websocat ws://localhost:27000/ws/transcribe < path_to_your_audio_file.wav
```

请将`path_to_your_audio_file.wav`替换为您要发送的音频文件的路径。

## 参考资料

- [ModelScope官方文档](https://www.modelscope.cn/docs)  
- [FunASR语音识别工具包](https://github.com/alibaba-damo-academy/FunASR)

## 问题反馈

如果您在使用过程中遇到任何问题,欢迎在GitHub上提交issue,我们会尽快回复。如果您有任何改进建议或新功能需求,也欢迎提交PR贡献代码。

希望本项目对您的工作和学习有所帮助!如有任何疑问,请随时联系我们。
