# Video2Edge: An Opensource Offloading Framework for Video Analytics on Edge

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

<img src="https://raw.githubusercontent.com/cap-ntu/Morph/master/DOC/system.png" width="40%" height="40%">

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


## Advanced Usage
We can start the controller to dynamically control the transcoding workers. To do this, we first need to add the information of the available VM instances or containers to the file **vm.list**. In this file, each line corresponds to the host name of an instance or a container. We can execute the command **hostname** to obtain the name of an instance or a container, and then, file the host name into the file **vm.list**. After that, we can start the controller.
```bash
python controller.py
```
We can observe the state of each worker in the MySQL database.
```bash
use morph
select * from server_info;
```
The worker node will read the value of the field **state** from the database to control itself. 

## Performance
The duration of the test video file is 138 minutes. The resolution is 1920x1080, and the bitrate is 2399 kb/s. The video data is encoded in H.264, and the audio data is encoded in AAC. The CPU frequency of the servers is 2.10GHz. The master node is allocated with 8 CPU cores, and the memory size is 8GB. The worker node is allocated with 4 CPU cores, and the memory size is 2GB. We use the Docker for the resource allocation. 

We first measure the video segmentation time for splitting the video file into equal-duration video blocks. The duration of each video block is 2 minutes. The FFmpeg command for the video segmentation is show as follow:

```bash
ffmpeg –i PV4h.mp4 -f segment -segment_time 120 -c copy -map 0 -segment_list PV4h.list PV4h_%03d_.mp4
```

The video segmentation time for the video file is 46 seconds.

We then measure the transcoding time for the test video file with different number of transcoding workers. The target resolution is 480x360. We illustrate the transcoding time in the following table:

| Worker Number  | FFmpeg | 1 | 5     | 10    | 15    | 20    | 25    | 30    |
|------------------   |------  |------ |------   |------   |------   |------   |------   |------   |
| Transcoding Time (s)  | 1775 | 1843 | 605   | 369   | 271   | 213   | 194   | 181   |
| Speed-up Ratio    | 1x  | 0.96x | 2.9x  | 4.8x  | 6.5x  | 8.3x  | 9.1x  | 9.8x  |

The transcoding time for using a standalone FFmpeg on a single server is 1775 seconds. If the system has only one active worker, the transcoding time is 1843 seconds, which is larger than the standalone ffmpeg. The overhead comes from the video segmentation, transmission, and concentration for transcoding the video file in a distributed manner. With more active workers to transcode the video blocks in parallel, the overall transcoding time decreases, achieving larger speed-up ratio. 

The FFmpeg command for video block concentration is as follow
```bash
ffmpeg -f concat –i PV4h_480x360.list -c copy PV4h_480x360.mp4
```
The video block concentration time is 13 seconds. 



## License
THIS SOFTWARE IS RELEASED UNDER THE MIT LICENSE (MIT)
Copyright (c), 2015, NTU CAP

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact
If you find any problem with this software, please feel free to contact us, your feedback is appreciated. 

Email: guanyugao@gmail.com; ggao001@e.ntu.edu.sg








