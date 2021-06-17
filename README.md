## SmartEye - An Open Source Framework for Real-Time Video Analytics with Edge-Cloud Collaboration


## Contents 
-------------------
* [Overview](#overview)
* [Workflow](#workflow)
* [Installation](#installation)
* [Programming Interface](#programming-interface)
* [Basic Usage](#basic-usage)
* [Advanced Usage](#advanced-usage)
* [Performance](#performance)
* [License](#license)
* [Contact](#contact)

## Overview
Video2Edge is an opensource offloading framework for video analytics on edge. It can leverage the scalability of the cloud infrastructure to encode and transcode the video files in fast speed, and dynamically provision the computing resource to accommodate the time-varying workload. Video2Edge is implemented in Python. It can be accessed via RESTful API, command line interface (CLI), and RPC. 

The system architecture is shown in the following figure. The system is composed of the following layers:

<img src="https://raw.githubusercontent.com/MSNLAB/SmartEye/master/DOC/smarteye.png?token=ACM3B7KTTTTJRH7XAFH6MHLAZN76C" width="60%" height="60%">

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

* [ubuntu 18.04](http://releases.ubuntu.com/14.04/)
* [Python 3](https://www.python.org/download/releases/2.7.6/)


Please click the above links for the installation of the dependent software.

It may require to install some lacked libraries, e.g., opencv, torchvision, torch, psutil, grpc, flask.
```bash
sudo apt update    
sudo apt install python-opencv
sudo apt install torchvision
sudo apt install torch
sudo apt install psutil
sudo apt install grpc
sudo apt install flask
```

Step 1: Clone the code from Github

```bash
git clone git@github.com:MSNLAB/video2edge.git
```

Step 2: Revise the configuration file **video2edge/config/config.ini**

All executable programs read the configuration information from config.ini.
Make sure each item is set with appropriate value according to your system configuration.
```bash

#the IP address of the servers
there are three servers in the configuration file, one is for forwarding server under the "transfer-url" label, 
others are for grpc servers or handled servers under the "handled-server" label. They are all initialized with "127.0.0.1"
Also, you can add more server urls under the "handled-server" label, it's ok. 
Under the "transfer-url" label, there are initial_url and picture_url, you just need to change the ip.
All the ports in the urls don't need to change, unless you want to change one.

#Should change ip address
[grpc-url]
url0=localhost:50051
url1=localhost:50051
[transfer-url]
initial_url=http://39.99.145.157:5000/initial
picture_url=http://39.99.145.157:5000/pictures_handler

#Remain unchanged
url0's port=50051
url1's port=50051
initial_url's=5000
picture_url's=5000

#Remain unchanged labels' content
[preload-models]
[image-classification]
[object-detection]
```

Step 3: For convenience, you can upload the whole project directly to each server  
```bash
#such as:
scp -r video2edge/ ****@ip_address:/home/user/video2edge
```
## Basic Usage

The easiest way to use this software is via command line. 

* Submit a image classification task by the command line  

Step 1: loading the project on forwarding server 
```bash
python3 ~/video2edge/server/forwarding_server.py
```

Step 2: loading the project on processing servers, there are more than one, but the execution is the same. 
```bash
python3 ~/video2edge/server/grpc/python/msg_transfer_service.py
```

Step 3: using the service on the client end
```bash
python3 main.py
```
According to the tips information， you can input the video you want to process, and input some parameters for your demand.  





## License
THIS SOFTWARE IS RELEASED UNDER THE MIT LICENSE (MIT)
Copyright (c), 2021, NUST SCE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact
If you find any problem with this software, please feel free to contact us, your feedback is appreciated. 

Email: guanyugao@gmail.com; gygao@njust.edu.cn









