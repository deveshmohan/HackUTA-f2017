# HackUTA-f2017

Visual motion tracking for disaster relief efforts. The KinectCam has 2 purposes: 1. security tracking for supply rooms, and, 2. using face recognition to detect persons in a disaster area for rescuing misssions

Dependencies: gcc, python 2.7, opencv, libfreenect, libhdf5, ffmpeg, apache web server, python2-pillow
Web client includes code from (hls.js)[https://github.com/video-dev/hls.js]

How to install
--

* Install the dependencies above
* Clone this repository into a new directory.
* Run `build.sh` to build the video capture tool.
* Copy and edit `email.cfg` to set up email notifications
* Configure the apache httpd server to serve the `http` directory

How to run
--

* Connect a Kinect device to usb
* Run `run.sh` to start the video transcoding

