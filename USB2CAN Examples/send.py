##############################################################################

## Description :  This codes is for test two USB2CAN module commuincation
##                one as sender and the other as receiver.
##                sender send  '0,1,2,3,4,5,6'
 
## Author      :  Calvin (calvin@inno-maker.com)/ www.inno-maker.com
              
                
## Date        :  2019.11.30

## Environment :  Hardware            ----------------------  Raspberry Pi 4
##                SYstem of RPI       ----------------------  2019-09-26-raspbian-buster-full.img
##                Version of Python   ----------------------  Python 3.7.3(Default in the system)
## Toinstall dependencies:
## sudo pip install python-can


###############################################################################


import os
import can
from time import sleep

#check system name, in linux will print 'posix' and in windows will print 'nt'
print(os.name)


os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')

forward = [0x23, 0x7A, 0x60, 0x00, 0x50, 0x46, 0x00, 0x00]
backward = [0x23, 0x7A, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00]
runOn = [0x2B, 0x40, 0x60, 0x00, 0x2F, 0x00, 0x00, 0x00]
runOff = [0x2B, 0x40, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00]

msg = can.Message(arbitration_id=0x01, data=forward, extended_id=False)
can0.send(msg)
msg = can.Message(arbitration_id=0x01, data=runOn, extended_id=False)
can0.send(msg)
sleep(1)
msg = can.Message(arbitration_id=0x01, data=backward, extended_id=False)
can0.send(msg)
msg = can.Message(arbitration_id=0x01, data=runOff, extended_id=False)
can0.send(msg)




os.system('sudo ifconfig can0 down')

