# 2017_Vision

A RaspberryPi running a python script was used with a Microsoft LifeCam HD-3000 for vision processing. OpenCV was the vision processing library, and WPILib's network tables were used to pass data from the Pi to the RoboRIO. The post-processing code to analyse the data pased to the RoboRIO can be seen in [here](https://github.com/2374/2017_Season/blob/master/2017_Season/src/org/usfirst/frc/team2374/robot/subsystems/Vision.java), and the rest of the robot code can be seen [here](https://github.com/2374/2017_Season).

## initalizeCamersha.sh

This script is called before vis_rect.py runs to set the camera to the proper settings.

## vis_calibrator.py

This script is use to calibrate the vis_rect.py, the main vision processing script, to the hsv threshold of the target. After a calibration, the hsv values were updated in vis_rect.py.

## vis_rect.py

This is the main vision processing script that outputs arrays of x and y coordinates, widths, and heights of the seen targets. In this case, each rectangle is viewed as a separate target. The arrays are passed to network tables hosted by the roboRIO.
