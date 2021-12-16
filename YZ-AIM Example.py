from YZ_AIM_DRIVER import YZ_AIM_Motor_Network
import logging

if __name__ == "__main__":

    logging.basicConfig(level=logging.ERROR)
        
    motorNetwork = YZ_AIM_Motor_Network()
    
    motorNetwork.add_motor(0x01)
    

    try:
        while(True):
            positionReached = False
            position = input("Enter new position: ")            
            motorNetwork.set_motor_position(0x01, int(position), blocking=True)        

    except KeyboardInterrupt:
        # stop motors
        motorNetwork.disarm_all_motors()

    except Exception as error:
        logging.error("ERROR OCCURED:", error)

    finally:
        motorNetwork.shutdown()
        logging.info("Shutting down network...")
    