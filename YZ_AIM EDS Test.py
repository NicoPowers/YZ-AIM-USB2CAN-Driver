import os
import canopen
import logging
import time
from canopen.network import Network
from canopen.nmt import NMT_STATES
from canopen.node.remote import RemoteNode
from canopen.profiles.p402 import BaseNode402


def print_speed(message):
    print('%s received' % message.name)
    for var in message:
        print('%s = %d' % (var.name, var.raw))

logging.basicConfig(level=logging.INFO)

os.system('sudo ifconfig can0 down')
time.sleep(1)

#Set CAN0 speed to 1M bps
os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

time.sleep(1)

motorNetwork = Network()

motorNetwork.connect(channel='can0', bustype='socketcan', bitrate=1000000)

motor_1 = motorNetwork.add_node(RemoteNode(1, "YZ_MOTOR.eds", False))
# motor_1.load_configuration()
# motor_1.rpdo.read()

motor_1.nmt.state = 'PRE-OPERATIONAL'

motor_1.rpdo[1].read()

motor_1.rpdo[1]['Controlword'].phys = 0x2F
motor_1.rpdo[1]['Modes of operation'].phys = 0x1
motor_1.rpdo[1]['Target position'].phys = 0

motor_1.rpdo[1].start(1)
motor_1.nmt.state = 'OPERATIONAL'

# print(int.from_bytes(motor_1.sdo.upload(0x1018, 1), 'little'))
# None
# motor_1.tpdo.read()
# motor_1.rpdo.read()
# motor_1.rpdo[1]['ControlWord'].raw = 0xF
# motor_1.rpdo[1] ['Target position'].phys = 1000000
# motor_1.nmt.state = 'OPERATIONAL'











