#!/bin/bash
apt-get update
apt-get install -y $(cat packages.txt)
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
pip install protobuf==4.25.3 --no-cache-dir
pip install grpcio==1.71.0 --no-cache-dir 