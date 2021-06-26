## SmartEye: An Open Source Framework for Real-Time Video Analytics with Edge-Cloud Collaboration


## Contents 
-------------------
* [Overview](#overview)
* [Workflow](#workflow)
* [Installation](#installation)
* [Programming Interface](#programming-interface)
* [Usage](#basic-usage)
* [Performance](#performance)
* [License](#license)
* [Contact](#contact)

## Overview

<img src="https://raw.githubusercontent.com/GuanyuACT/Public/master/smarteye.png" width="60%" height="60%">

* client section

The client section 

The client mainly includes three functions: one is the file reading interface, which is used to read the video files to be processed. The second is the decision engine, which determines the resolution and other information according to the current network state (network speed, delay, etc.). The third is the preprocessing function, which preprocesses the image file according to the decision result of the decision engine; Fourth, the local processing function, for some simple structure of the image, can be directly processed locally, do not have to send to the server.

* forwarding server

It receives data from the client and sends the data to a processing server for processing through a series of decisions. The decision-making method includes random selection and selection according to the CPU utilization of each server. Then get the processing result and return it to the client.

* Processing server

The processing server consists of two parts, one is data preprocessing, which can process the image into usable format. The second part is the prediction part, which includes two functions：image recognition and object detection, both of which are processed by the pre training model in pytorch.

## Workflow

<img src="https://raw.githubusercontent.com/cap-ntu/Morph/master/DOC/workflow.png" width="80%" height="80%">

The user submits a processing task by providing the video path, being read by virtual camera or derectly video interface. Together with some other parameters, such as service type(image classification or object detection), the client will be initialized. At the same time, preprocessing module, local process module, decision engine module and local store module will be initialized too. In this time, client will get the current network condition, for example, service delay, net speed. Then, Decision Engine makes some decisions for data transfer, such as image resolution. And client will transfer these information to preprocess module. And the preprocess module processes the images according to the parameters. Last, client transfer these images which have been processed to the transfer server. For some images of simple structure, i preserve local process interface. 

Once the forwarding server get the data from client, the server will decide to send to which Processing server and send data to it.

when the processing server get the data from forwarding server, the server will preprocess the data first, letting the image conform to the format of predictions. Then processing server will make predictions respectively. Last, return the results to forwarding server.

forwarding server return the result directly to the client,and the client will print the result or store the result respectively according to the service type. 

## Installation

System Requirement

* [ubuntu 18.04](http://releases.ubuntu.com/18.04/)
* [Python 3.6.9](https://www.python.org/downloads/release/python-369/)
* [Jetpack 4.5](https://developer.nvidia.com/jetpack-sdk-45-archive)
* [cuda 11.0](https://developer.nvidia.com/cuda-11.0-update1-download-archive?target_os=Linux&target_arch=x86_64)
* [pytorch 1.8.0](https://pytorch.org/)

Please click the above links for the installation of the dependent software.

It may require to install some lacked libraries, e.g., opencv, torchvision, torch, psutil, grpc, flask.
There are three parts in this installation:

part 1: install libraries in Jetson TX2, as edge cloud.
```bash
sudo apt update
pip3 install loguru
pip3 install psutil
pip3 install configparser
pip3 install opencv-contrib-python
```

part 2: install libraries in transfer server.
```bash
sudo apt update
sudo apt install grpc
sudo apt install flask
pip3 install apscheduler
pip3 install loguru
```

part 3: install libraries in backend server.
```bash
pip3 install loguru
pip3 install psutil
pip3 install grpcio
pip3 install grpcio-tools googleapis-common-protos
```
## Usage

Step 1: Clone the code from Github

```bash
git clone git@github.com:MSNLAB/SmartEye.git
```
Step 2: Revise the configuration file **SmartEye/config/config.ini**

All executable programs read the configuration information from config.ini.
Make sure each item is set with appropriate value according to your system configuration.
```bash

#the IP address of the servers
there are three servers in the configuration file, one is for frontend server under the "flask-url" label, 
others are for grpc servers or handled servers under the "grpc-url" label. They are all initialized with "127.0.0.1"
Also, you can add more server urls under the "grpc-url" label, it's ok. 
For the servers,  you just need to change the ip of yours.
All the ports in the urls don't need to change, unless you want to change one.

#Should change ip address
[grpc-url]
url0=127.0.0.1:50051
url1=127.0.0.1:50051
[flask-url]
video_frame_url=http://127.0.0.1:5000/image_handler

#Remain unchanged
url0's port=50051
url1's port=50051
initial_url's=5000

#Remain unchanged labels' content
[preload-models]
[image-classification]
[object-detection]
```

Step 3: For convenience, you can upload the whole project directly to each server  
```bash
#such as:
scp -r SmartEye/ your_account@ip_address:/home/user/
```
The easiest way to use this software is via command line. 

* To execute a video process task, there are three steps to go:  

Step 1: loading the project on every grpc server. if you have more than one grpc servers, load them one by one. Remember to change it to your own graphics card number.
```bash
cd ~/SmartEye/backend_server/
CUDA_VISIBLE_DEVICES=your_nvidia_number python3 rpc_server.py
```

Step 2: loading the project on the flask server. 
```bash
cd ~/SmartEye/frontend_server/
nohup python3 forwarding_server.py
```

Step 3: execute your task in the TX, the edge.
According to the tips information， you can input the video you want to process, and input some parameters for your demand.
```bash
#such as
cd ~/SmartEye
python3 edge_main -f your_video -s 1 -i 50
```
  





## License
THIS SOFTWARE IS RELEASED UNDER THE MIT LICENSE (MIT)
Copyright (c), 2021, NUST SCE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact
If you find any problem with this software, please feel free to contact us, your feedback is appreciated. 

Email: guanyugao@gmail.com; gygao@njust.edu.cn









