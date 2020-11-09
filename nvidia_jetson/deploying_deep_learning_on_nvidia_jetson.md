* Draft: 2020-10-13 (Tue)

# Deploying Deep Learning on NVIDIA Jetson

 at [dusty-nv](https://github.com/dusty-nv)/[jetson-inference](https://github.com/dusty-nv/jetson-inference)

[Hello AI World](https://github.com/dusty-nv/jetson-inference/blob/master/README.md#hello-ai-world)



https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-example-python-2.md

https://blog.naver.com/PostView.nhn?blogId=makepluscode&logNo=221563018517&parentCategoryNo=&categoryNo=49&viewDate=&isShowPopularPosts=true&from=search

https://blog.naver.com/PostView.nhn?blogId=makepluscode&logNo=221399939583&parentCategoryNo=&categoryNo=49&viewDate=&isShowPopularPosts=true&from=search

https://blog.naver.com/PostView.nhn?blogId=makepluscode&logNo=221403126394&parentCategoryNo=&categoryNo=49&viewDate=&isShowPopularPosts=true&from=search



#### System Setup

- [Setting up Jetson with JetPack](https://github.com/dusty-nv/jetson-inference/blob/master/docs/jetpack-setup-2.md)
- [Running the Docker Container](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md) (Done)
- [Building the Project from Source](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md) (Done)

#### Inference

- [Classifying Images with ImageNet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-console-2.md)
  - [Using the ImageNet Program on Jetson](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-console-2.md) (Done)
    - [Model Download Mirror](https://github.com/dusty-nv/jetson-inference/releases/tag/model-mirror-190618)
  - [Coding Your Own Image Recognition Program (Python)](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-example-python-2.md) (Done)
  - [Coding Your Own Image Recognition Program (C++)](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-example-2.md)
  - [Running the Live Camera Recognition Demo](https://github.com/dusty-nv/jetson-inference/blob/master/docs/imagenet-camera-2.md)
- Locating Objects with DetectNet
  - [Detecting Objects from Images](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-console-2.md#detecting-objects-from-the-command-line)
  - [Running the Live Camera Detection Demo](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-camera-2.md)
  - [Coding Your Own Object Detection Program](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-example-2.md)
- Semantic Segmentation with SegNet
  - [Segmenting Images from the Command Line](https://github.com/dusty-nv/jetson-inference/blob/master/docs/segnet-console-2.md#segmenting-images-from-the-command-line)
  - [Running the Live Camera Segmentation Demo](https://github.com/dusty-nv/jetson-inference/blob/master/docs/segnet-camera-2.md)

#### Training

- [Transfer Learning with PyTorch](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-transfer-learning.md)
- Classification/Recognition (ResNet-18)
  - [Re-training on the Cat/Dog Dataset](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-cat-dog.md)
  - [Re-training on the PlantCLEF Dataset](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-plants.md)
  - [Collecting your own Classification Datasets](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect.md)
- Object Detection (SSD-Mobilenet)
  - [Re-training SSD-Mobilenet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)
  - [Collecting your own Detection Datasets](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-collect-detection.md)

#### Appendix

- [Camera Streaming and Multimedia](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-streaming.md)
- [Image Manipulation with CUDA](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-image.md)
- [Deep Learning Nodes for ROS/ROS2](https://github.com/dusty-nv/ros_deep_learning)