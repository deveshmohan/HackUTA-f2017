#!/bin/sh
ffmpeg -framerate 30 -pix_fmt rgb24 -video_size 640x480 -f rawvideo -i pipe:0 -map 0 -c:v libx264 -pix_fmt yuv420p -b:v 128k -f segment -segment_time 5 -segment_list http/stream/segments.m3u8 -segment_format mpeg_ts -segment_list_type m3u8 -y http/stream/segment_%05d.ts
