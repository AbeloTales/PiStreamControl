#!/bin/bash
/usr/bin/ffmpeg -f v4l2 -thread_queue_size 1024 -video_size 1280x720 -framerate 30 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -b:v 2.5M -pix_fmt yuv420p -f mpegts "srt://192.168.100.37:5000?mode=caller&latency=50000"
