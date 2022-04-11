import os
import time
import logging
import canopen
from canopen.network import Network
from canopen.profiles.p402 import BaseNode402

os.system('sudo ifconfig can0 down')
time.sleep(1)

#Set CAN0 speed to 1M bps
os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')


logging.basicConfig(level=logging.ERROR)


some_node = BaseNode402(1, 'YZ_MOTOR.eds')
network = Network()

network.connect(channel='can0', bustype='socketcan', bitrate=1000000)
network.add_node(some_node)

time.sleep(5)

some_node.nmt.state = 'RESET COMMUNICATION'
#node.nmt.state = 'RESET'
some_node.nmt.wait_for_bootup(15)


print('node state 1) = {0}'.format(some_node.nmt.state))

# run the setup routine for TPDO1 and it's callback
some_node.setup_402_state_machine()


# Iterate over arrays or records
error_log = some_node.sdo[0x1001]
for error in error_log.values():
    print("Error {0} was found in the log".format(error.raw))



for node_id in network:
    print(network[node_id])




print('node state 2) = {0}'.format(some_node.nmt.state))

# Read a variable using SDO

# node.sdo[0x1006].raw = 1
# node.sdo[0x100c].raw = 100
# node.sdo[0x100d].raw = 3
# node.sdo[0x1014].raw = 163
# node.sdo[0x1003][0].raw = 0