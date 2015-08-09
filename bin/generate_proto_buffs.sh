#!/bin/bash

mkdir -p build/proto/python/
protoc -I=proto --python_out=build/proto/python proto/*.proto
# Copy everything to the right locations
mkdir server/proto
cp -r build/proto/python/proto/*.py server/proto
