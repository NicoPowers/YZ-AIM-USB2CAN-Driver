# YZ-AIM-USB2CAN-Driver

## TODO:
1) change motor id of connected motors 
2) receive voltage, current, and torque readings from motor
3) alter trapezodial speed/acceleration curves of motors
4) see if there's a way to fine tune PID parameters

Right now this only allows basic functionality of set position and reading the position and blocking the code until the position is reached. The program return the actual position instead of the theoretical position so you can account for that in your code.
Since it is written in Python is should be fairly easy to integrate with ROS 1 or ROS 2.

This only works for Linux.

This also requires a USB2CAN device or other similar USB-CAN interface that allows the CAN port to show up on the PC.




