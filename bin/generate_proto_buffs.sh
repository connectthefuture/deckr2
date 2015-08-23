#!/bin/bash

mkdir -p build/proto/python/
protoc -I=proto --python_out=build/proto/python proto/*.proto
# Copy everything to the right locations
mkdir -p server/proto
cp -r build/proto/python/*.py server/proto
