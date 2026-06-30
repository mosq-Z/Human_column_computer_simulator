#士兵的常数
from math import *



basic_time = 8   #方便成倍调整士兵动作耗时

Soldier_vision = 50
Soldier_volume = 0.2  #士兵的视野半径和体积，单位m
Soldier_turning_time = 0.08*basic_time #转向延迟，单位s/弧度
Soldier_thinking_time = 0.02*basic_time   #思考时间，单位s
Soldier_flag_time = 0.04*basic_time #士兵举旗旗子用的时长s

