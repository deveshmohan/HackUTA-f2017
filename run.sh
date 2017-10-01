#!/bin/sh
mkdir -p http/stream
mkdir -p http/gallery
rm http/stream/*
./capture.sh | ./transcode.sh

