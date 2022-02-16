# tequ-tf1-ca-training-pipeline
This guide is for configuring your Windows machine to train Tensorflow.js models. Guide assumes that source image files are annotated with Cloud Annotations tool (https://cloud.annotations.ai/). 

Colab notebook https://colab.research.google.com/github/cloud-annotations/google-colab-training/blob/master/object_detection.ipynb has been used as template for this pipeline and functionality of this notebook has been transferred to work offline on Windows machine.

## Requirements

- Windows OS (Windows 10 & Windows 2019 server are tested)
- NVIDIA GPU (Quadro P600 and Tesla P100 are tested)

## Configuration

### 1. Download and install following software.

| Software      | Version       | Link |
| ------------- |:-------------:| :-------------:| 
| CUDA          | 10.0.130      | https://developer.nvidia.com/cuda-downloads |
| cuDNN         | 7.6.5.32      | https://developer.nvidia.com/cudnn |
| Protoc        | 3.17.3        | https://developers.google.com/protocol-buffers/docs/downloads |
| Python        | 3.7.9         | https://www.python.org/downloads/release/python-379/ |
| Git           | 2.33.0        | https://git-scm.com/downloads |
| GPU drivers   | Supported driver for Cuda 10 | https://www.nvidia.com/Download/index.aspx?lang=en-us |

### 2. cuDNN installation

Copy extracted files to CUDA Toolkit installation folder following the same folder structure.

Copy extracted files in folder ```Cuda\bin``` to ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin```

Copy extracted files in folder ```Cuda\lib``` to ```C::\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\lib```

Copy extracted files in folder ```Cuda\include``` to ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\include```

You could also setup environment variables to point the location of cuDNN files to make things work.

### 3. Clone this project 

```
git clone https://github.com/juhaautioniemi/tequ-tf1-ca-training-pipeline.git
```

### 4. Navigate to project folder

Run batch-files

```1. Install Python libraries.cmd```

```2. Clone models repository.cmd```

```3. Build object detection api.cmd```

```4. Setup environment variables.cmd```

### 5. Get source files

- Export your Cloud Annotations project as ZIP-file
- Unzip files to C:\<your project folder>\content\ca_source_data

### 6. Run training process

- Navigate to project folder
- Run batch-file ```Run training process.cmd```
- Input requested values during process (base model, batch size, training steps)
- Trained & converted Tensorflow.js models are saved in ```C:\<your project folder>\content\trained_models```

### 7. Using the model

Model files can be loaded and executed in Node-RED with 

https://flows.nodered.org/node/node-red-contrib-cloud-annotations-gpu
or
https://flows.nodered.org/node/node-red-contrib-tf-model

More information:
https://github.com/juhaautioniemi/jetson-nodered-tensorflow
https://github.com/juhaautioniemi/win10-nodered-tensorflow

