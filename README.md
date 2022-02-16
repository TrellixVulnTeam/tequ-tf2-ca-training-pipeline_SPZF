This repository is developed in Fish-IoT project

https://www.tequ.fi/en/project-bank/fish-iot/ 

---

# Description 

This guide is for configuring your Windows machine to train Tensorflow.js models. Guide assumes that source image files are annotated with Cloud Annotations tool (https://cloud.annotations.ai/). 

Colab notebook https://colab.research.google.com/github/cloud-annotations/google-colab-training/blob/master/object_detection.ipynb has been used as template for this pipeline and functionality of this notebook has been transferred to work offline on Windows machine.

# Requirements

- Windows OS (Windows 10 & Windows 2019 server are tested)
- NVIDIA GPU (Quadro P600 and Tesla P100 are tested)

# Configuration

## 1. Download and install following software.

| Software      | Version       | Link |
| ------------- |:-------------:| :-------------:| 
| CUDA          | 11.6.0_511.23 | https://developer.nvidia.com/cuda-downloads |
| cuDNN         | 8.3.2.44      | https://developer.nvidia.com/cudnn |
| Protoc        | 3.19.4        | https://developers.google.com/protocol-buffers/docs/downloads |
| Python        | 3.10.2        | https://www.python.org/downloads/release/python-379/ |
| Git           | 2.35.1        | https://git-scm.com/downloads |
| GPU drivers   | Supported driver for Cuda 11 | https://www.nvidia.com/Download/index.aspx?lang=en-us |


CUDA & cuDNN installation steps are documented in following repository:

https://github.com/juhaautioniemi/win10-nodered-tensorflow


## 2. Open command line and clone this project 

```
cd\
```

```
git clone https://github.com/Lapland-UAS-Tequ/tequ-tf2-ca-training-pipeline.git
```

## 3. Run batch-files to setup environment

```
cd c:\tequ-tf2-ca-training-pipeline
```


```
1. Install Python libraries.cmd
```

```
2. Clone models repository.cmd
```

```
3. Build object detection api.cmd
```

```
4. Setup environment variables.cmd
```

```
5. Run protoc.cmd
```

## 4. Get source files

- Export your Cloud Annotations project as ZIP-file
- Unzip files to C:\tequ-tf2-ca-training-pipeline\content\ca_source_data


# Training the model

- Navigate to project folder
- Run batch-file ```Run training process.cmd```
- Input requested values during process (base model, batch size, training steps)
- Trained Tensorflow saved models will located in ```C:\tequ-tf2-ca-training-pipeline\content\trained_models```


# Using the model

Model files can be loaded and executed for example in Node-RED with 

https://github.com/juhaautioniemi/win10-nodered-tensorflow

https://github.com/Lapland-UAS-Tequ/tequ-jetson-nodered-tensorflow

https://github.com/Lapland-UAS-Tequ/tequ-setup-triton-inference-server

