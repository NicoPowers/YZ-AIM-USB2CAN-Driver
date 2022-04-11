# YZ-AIM-USB2CAN-Driver

Instal net-tools
Install canopen for Python 3

# ALERTS
read_response from canopen/sdo/client.py raises SdoCommunicationError, but is not handled in pdo read function in canopen/pdo/base.py
## TODO:
1) change motor id of connected motors 
2) receive voltage, current, and torque readings from motor
3) alter trapezodial speed/acceleration curves of motors
4) see if there's a way to fine tune PID parameters

Right now this only allows basic functionality of set position and reading the position and blocking the code until the position is reached. The program return the actual position instead of the theoretical position so you can account for that in your code.
Since it is written in Python is should be fairly easy to integrate with ROS 1 or ROS 2.

This only works for Linux.

This also requires a USB2CAN device or other similar USB-CAN interface that allows the CAN port to show up on the PC.

You can ignore the USB2CAN examples, that was just to help setup the ports for CAN.

The translated datasheet is also here as a PDF, it did not translate perfectly so the images are missing. 

The .eds file is supposed to be used with CANOpen so the bus can know what parameters are available to read/write to each motor, but doesn't seem to be very useful as of now.

I am probably controlling this incorrectly, but for now it's working. Ideally we should just be able to write and read to those parameters specified in the .eds file and it should be more abstracted than setting the byte array and appending the position value bytes.



