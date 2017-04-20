#!/bin/bash

v4l2-ctl --device=/dev/video1 -c exposure_auto=1
v4l2-ctl --device=/dev/video1 -c exposure_absolute=5
v4l2-ctl --device=/dev/video1 -c brightness=30
