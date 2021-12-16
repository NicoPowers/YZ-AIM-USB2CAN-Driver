# YZ-AIM-USB2CAN-Driver

## TODO:
1) change motor id of connected motors 
2) receive voltage, current, and torque readings from motor
3) alter trapezodial speed/acceleration curves of motors
4) see if there's a way to fine tune PID parameters

Right now this only allows basic functionality of set position and reading the position and blocking the code until the position is reached. The program return the actual position so you can account for that in your code.
Since it is written in Python is should be fairly easy to use wth ROS 1 or ROS 2.

This only works and has been tested on Linux.


