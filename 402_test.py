import os
import canopen
import logging
import time
import binascii
from canopen.network import Network
from canopen.nmt import NMT_STATES
from canopen.node.remote import RemoteNode
from canopen.profiles.p402 import BaseNode402

#Set CAN0 speed to 1M bps
# os.system('sudo ip link set can0 type can bitrate 1000000')
# os.system('sudo ifconfig can0 up')

network = canopen.Network()
network.connect(channel='can0', bustype='socketcan')

some_node = BaseNode402(1, 'YZ_MOTOR.eds') 
# network.add_node(some_node)
some_node.associate_network(network)
# run the setup routine for TPDO1 and it's callback
some_node.setup_402_state_machine()

# os.system('sudo ifconfig can0 down')