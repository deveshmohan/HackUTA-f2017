#!/bin/sh
ffmpeg -framerate 30 -pix_fmt rgb24 -video_size 640x480 -f rawvideo -i pipe:0 -map 0 -c:v libx264 -pix_fmt yuv420p -b:v 128k -f hls -hls_flags delete_segments -hls_time 1 -hls_list_size 4 http/stream/segments.m3u8
