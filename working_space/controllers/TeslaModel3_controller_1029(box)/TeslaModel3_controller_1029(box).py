# from vehicle import Driver # <- inherit from this class
# from controller import GPS # <- Not need
# from controller import Supervisor
from vehicle import Driver
import numpy as np
from get_information import parse_proto, get_value

import json

def convert_json(input : dict):
    with open("data.json", "w") as f:
        json.dump(input, f)

# Supervisor 객체 생성
driver = Driver()

# 차량 및 건물 노드 접근
car_node = driver.getFromDef("TeslaModel3")  # 'car'는 정확한 DEF 이름이어야 함

# building position information
building_names = ["commercial_building", "fast_food_restaurant", "museum", "hotel", "church", "residential_tower", "residential_tower(1)"]
tree_names = ['tree(1),']
# TODO : (우선순위 낮음) 사람이 직접 def 입력 안하는 방법

tesla_array = np.array([])

fixed_dict = {
    'building_dict' : {},
    'tree_dict' : {},
    'light_dict' : {},
    'person_dict' :{},
    'car_dict' : {} # Telsa 제외 다른 차량 (주차되어있는 차량, 빨간 불 멈춤)
}


building_dict = {}     # 노드를 저장할 리스트
# building_nodes = []     # 노드를 저장할 리스트
# building_position = []  # 위치를 저장할 리스트
for name in building_names:
    node = driver.getFromDef(name)
    
    file_name = '../../protos/' + name + '.proto'
    print(file_name)
    with open(file_name, "r") as file:
        proto_content = file.read()
    proto_dict = parse_proto(proto_content)

    fixed_dict['building_dict'][name] = {
        'pos' : node.getPosition(),
        'ori' : node.getOrientation(),
        'size' : get_value(proto_dict, 'size'),
    }   
    # building_nodes.append(node)  # 노드 저장
    # building_position.append(position)
    if node is not None:
        print(f"bounding box of {name}:", fixed_dict['building_dict'])
    else:
        print(f"{name} not found")

convert_json(fixed_dict)


#for name in tree_names:
  #   fixed_dict['tree_dict'][name] = {


driver.setSteeringAngle(0.2)  # 차량 조향 각도
driver.setCruisingSpeed(20)   # 차량 속도


while driver.step() != -1:  
    print('\n\n-------- START -------')
    print("Time: ", driver.getTime())  # 시뮬레이션 경과 시간(sec)
    
    # 차량 정보
    print("\nSpeed : ", driver.getCurrentSpeed())              # 속력 (m/s)
    print("\nPosition : ", car_node.getPosition())             # 위치 (x, y, z)
    print("\nOrientation : ", car_node.getOrientation())       # 방향 matrix
    print("\nTransformation matrix :\n", car_node.getPose())   # 방향, 위치 matrix
    tesla_array = np.array(car_node.getPose())
    print(type(car_node.getPose()))
    print(type(tesla_array))
    print(fixed_dict['building_dict']['museum'])


    print('-------- END --------')












































