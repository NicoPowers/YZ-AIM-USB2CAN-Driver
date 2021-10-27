import os
import canopen
import logging
import time
import binascii
from canopen.network import Network
from canopen.nmt import NMT_STATES
from canopen.node.remote import RemoteNode
from canopen.profiles.p402 import BaseNode402

class MotorNetwork(Network):    
    MOTOR_ON_CMD = [0x2B, 0x40, 0x60, 0x00, 0x2F, 0x00, 0x00, 0x00]
    MOTOR_OFF_CMD = [0x2B, 0x40, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00]    
    READ_POSITION_CMD = [0x40, 0x64, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00]
    SET_POSITION_CMD = [0x23, 0x7A, 0x60, 0x00]

    motors = {}

    def __init__(self):
        try:
            #Set CAN0 speed to 1M bps
            os.system('sudo ip link set can0 type can bitrate 1000000')
            os.system('sudo ifconfig can0 up')

            super().__init__()

            self.connect(channel='can0', bustype='socketcan')
            

        except Exception as error:
            print("ERROR: {}".format(error))
    
    def shutdown(self):
        self.disconnect()
        os.system('sudo ifconfig can0 down')

    def arm_motor(self, motor_id):
        self.send_message(0x600 + motor_id, self.MOTOR_ON_CMD)

    def disarm_motor(self, motor_id):
        self.send_message(0x600 + motor_id, self.MOTOR_OFF_CMD)

    def disarm_all_motors(self):
        for each_motor_id in self.motors.keys():
            self.disarm_motor(each_motor_id)

    def add_motor(self, motor_id):
        self.add_node(motor_id)
        self.motors.update({motor_id: [None, True]})
        
    def start_motor(self, motor_id):
        self.send_message(motor_id, [0x1, 0])
        self.nodes[motor_id].nmt.wait_for_heartbeat()
        assert self.nodes[motor_id].nmt.state == NMT_STATES[5]        
            
    def subscribe_motor_position(self, motor_id):
        self.subscribe(0x580 + motor_id, self.__motor_response_callback)
    
    def unsubscribe_motor_position(self, motor_id):
        self.unsubscribe(0x580 + motor_id)    

    def set_motor_position(self, motor_id, position, blocking=False):
        hexValue = format(position, 'x')        
        numDigits = len(hexValue)
        if (numDigits % 2 != 0):            
            hexValue = "0" + hexValue
        
        byteArray = bytearray.fromhex(hexValue)
        byteArray.reverse()        
        
        hexArray = self.SET_POSITION_CMD
        for eachByte in byteArray:
            hexArray.append(int(hex(eachByte), 16))
        
        self.send_message(0x600 + motor_id, hexArray)

        if blocking:
            self.subscribe_motor_position(motor_id)            
            while(self.motors[motor_id][1]):
                self.request_motor_position(motor_id)                
                print("Current position of motor {}: {}".format(motor_id, self.motors[motor_id][0]))
                time.sleep(0.1)

            print("Motor {} has finished traveling to theoretical position {}. Actual position is {} ".format(motor_id, position, self.motors[motor_id][0]))            
            self.unsubscribe_motor_position(motor_id)

                                
    def request_motor_position(self, motor_id):        
        self.send_message(0x600 + motor_id, self.READ_POSITION_CMD)

    def __motor_response_callback(self, node, response, timestamp):        
        position_response = bytearray(b'Cd`\x00')
        motor_id = node - 0x580
        logging.debug("Response from node {} at {}".format(hex(motor_id), timestamp))         
        
        if position_response in response:
            position = int.from_bytes(response[4::], "little")            
            logging.debug("Position = {}".format(position))            
            # check to see if this motor has stopped moving since last callback
            if self.motors[motor_id][0] == position:
                self.motors.update({(motor_id): [position, False]})                
            else:
                self.motors.update({(motor_id): [position, True]})                                  


if __name__ == "__main__":

    logging.basicConfig(level=logging.ERROR)
    
    motorNetwork = MotorNetwork()


    motorNetwork.add_motor(0x01)
    motorNetwork.start_motor(0x01)
    motorNetwork.arm_motor(0x01)

    try:
        while(True):
            positionReached = False
            position = input("Enter new position: ")
            motorNetwork.set_motor_position(0x01, int(position), blocking=True)        

    except KeyboardInterrupt:
        # stop motors
        motorNetwork.disarm_all_motors()

    except Exception as error:
        print("ERROR OCCURED:", error)

    finally:
        motorNetwork.shutdown()
        print("Shutting down network")

