FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

WORKDIR /workspaces/imgBookOcr

RUN apt-get update && \
  apt-get install -y --no-install-recommends git 

RUN git config --global --add safe.directory /app

RUN git config --global --add safe.directory /workspaces/imgBookOcr

RUN apt-get install -y tesseract-ocr tesseract-ocr-jpn

RUN pip install pytesseract Pillow

RUN cd /usr/share/tesseract-ocr/4.00/tessdata

RUN curl -LO https://github.com/tesseract-ocr/tessdata_best/raw/main/jpn.traineddata && \ 
    curl -LO https://github.com/tesseract-ocr/tessdata_best/raw/main/jpn_vert.traineddata

RUN cd /workspaces/imgBookOcr

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*
