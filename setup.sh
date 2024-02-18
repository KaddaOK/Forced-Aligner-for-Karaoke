#!/bin/bash 
Get_NeMo_Version="1.21"
NeMoBranch="v$Get_NeMo_Version.0"
sudo apt-get update
sudo apt-get install gcc ffmpeg build-essential python3-dev python3 python3-pip python-is-python3 -y
pip install cython ffmpeg pydub python-magic
pip install nemo_toolkit[all]==$Get_NeMo_Version
git clone -b $NeMoBranch https://github.com/NVIDIA/NeMo