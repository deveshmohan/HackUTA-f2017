#!/bin/sh
rm http/stream/*
./capture.sh | ./transcode.sh

