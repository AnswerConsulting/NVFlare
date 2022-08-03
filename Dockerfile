FROM nvidia/cuda:11.4.2-devel-ubuntu20.04

ARG VERSION=2.0.16

COPY app/site-1/ app/site-1

RUN ls -la \
    && apt update \
    && yes | apt-get install wget \ 
    && yes | apt install python3.8 \
    && yes | apt install python3-pip \
    && yes | apt-get install python3-venv \
    && python3 -m venv nvflare-env \
    && . nvflare-env/bin/activate \
    && python3 -m pip install -U pip \
    && python3 -m pip install -U setuptools \
    && python3 -m pip install nvflare==${VERSION} \
    && python3 -m pip install torch torchvision \
    && python3 -m pip install numpy \
    && python3 -m pip install pandas \
    && echo 'NVFlare client installation complete'
