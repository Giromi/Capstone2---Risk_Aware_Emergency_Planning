from vehicle import Driver
import numpy as np

driver = Driver()
car_node = driver.getFromDef("vehicle")  
driver.setCruisingSpeed(100)

while driver.step() != -1:
    orientation = car_node.getOrientation()
    rotation_matrix = np.array(orientation).reshape(3, 3)
    yaw = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    print("car yaw :", yaw)
    print('new')
    cur_delta = np.deg2rad(0)  
    print("current_delta:", cur_delta)
    driver.setSteeringAngle(cur_delta)