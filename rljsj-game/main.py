# ==========================调试转向运算的===================================
# from entities.soldier.soldier_calculations import turning_time_calculation
# print(turning_time_calculation(1,1,2,1,1,2,1))

# # ==========================调试基础常数和遮挡,穿模关系计算===================================
# from entities.soldier.soldier_generation import Soldier

# xiaomin = Soldier('小明',0,0.5,'and')
# xiaohong = Soldier('小红',0.5,0,'or')
# xiaozhuang = Soldier('小壮',0,0,'not')

# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaozhuang.update_ang()
# xiaozhuang.update_turning_time()
# xiaozhuang.update_if_12_invision()
# xiaozhuang.update_if_overlap()
# print(xiaozhuang.field_of_view_ang)
# # xiaomin.information()
# xiaohong.information()
# xiaozhuang.information()

# # ==========================调试接收和记忆===================================````
# from entities.soldier.soldier_generation import Soldier
# from math import *
# xiaomin = Soldier('小明',2,2,'and')
# xiaohong = Soldier('小红',-4,4,'or')
# xiaozhuang = Soldier('小壮',0,0,'not')
# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaozhuang.update_turning_time()
# print(xiaozhuang.t1_to_s_ang)
# print(xiaozhuang.t2_to_s_ang)

# xiaozhuang.t_ang = pi/4  #调试内容，看向小明
# xiaozhuang.update_receive_from_1_or_2()
# print(xiaozhuang.receive_from_1)
# print(xiaozhuang.receive_from_2)


# # xiaozhuang.t_ang = pi/4*3  #调试内容，看向小红
# # xiaozhuang.update_receive_from_1_or_2()
# # print(xiaozhuang.receive_from_1)  
# # print(xiaozhuang.receive_from_2)

# # xiaozhuang.t_ang = pi/4*3+0.1  #调试内容，那都不看
# # xiaozhuang.update_receive_from_1_or_2()
# # print(xiaozhuang.receive_from_1)  
# # print(xiaozhuang.receive_from_2)

# xiaomin.raise_flag = ['wanglinjun',True] #调试内容，小明举旗
# xiaozhuang.update_remenber_1_or_2()
# print(xiaozhuang.remenber_1)
# print(xiaozhuang.remenber_2)

# # ==========================调试帧更新===================================
# from entities.soldier.soldier_generation import Soldier
# from math import *
# xiaomin = Soldier('小明',2,2,'and')
# xiaohong = Soldier('小红',-4,4,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaozhuang.update_turning_time()
# xiaozhuang.update_ang()
# print(xiaozhuang.t1_to_s_ang)
# print(xiaozhuang.t2_to_s_ang)
# print(xiaozhuang.ang)
# for i in range(5000):
#     print(f'在{i}帧')
#     xiaozhuang.update_receive_from_1_or_2()
#     xiaozhuang.update_remenber_1_or_2()
#     xiaozhuang.update_t_thkig_time()
#     xiaozhuang.update_raise_flag() #接收 ，记忆，思考，举旗
#     xiaozhuang.update_t_ang()

#     if i == 100:
#         xiaohong.raise_flag = [1,True] #调试内容，小红在100帧举旗子，旗子上写的1
#     if i == 400:
#         xiaomin.raise_flag = [1,True] #调试内容，小明400帧举旗子，旗子上写的1
#     if xiaozhuang.remenber_1[1] and xiaozhuang.remenber_2[1]:
#         print('小壮正在思考')
#     if xiaozhuang.raise_flag[1]:
#         print(f'在{i}帧的时候，成功收集小红的{xiaozhuang.remenber_2[0]}，小明的{xiaozhuang.remenber_1[0]},并成功举旗为{xiaozhuang.raise_flag[0]}')
#         break

# #==========================调试层级更新===================================
# from entities.soldier.soldier_generation import Soldier
# from math import *
# xiaomin = Soldier('小明',2,2,'and')
# xiaohong = Soldier('小红',-4,4,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# xiaohei = Soldier('小黑',7,10,'and')
# xiaobai = Soldier('小白',-3,-10,'nor')
# xiaolan = Soldier('小兰',-4,-3,'not')

# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaohei.update_target12(xiaohong,xiaozhuang)
# xiaobai.update_target12(xiaohei,xiaomin)
# xiaolan.update_target12(xiaohong,xiaobai)

# Soldier.update_all_level()

# print(xiaomin.level)
# print(xiaohong.level)
# print(xiaozhuang.level)
# print(xiaohei.level)
# print(xiaobai.level)
# print(xiaolan.level)



# # ==========================调试初始化所有状态函数===================================
# from entities.soldier.soldier_generation import Soldier
# from math import *
# xiaomin = Soldier('小明',2,2,'and')
# xiaohong = Soldier('小红',-4,4,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# xiaohei = Soldier('小黑',7,10,'and')
# xiaobai = Soldier('小白',-3,-10,'nor')
# xiaolan = Soldier('小兰',-4,-3,'not')

# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaohei.update_target12(xiaohong,xiaozhuang)
# xiaobai.update_target12(xiaohei,xiaomin)
# xiaolan.update_target12(xiaobai,None)

# Soldier.Update_all_state()


# # ==========================调试单个士兵的帧操作打包===================================

# from entities.soldier.soldier_generation import Soldier
# from math import *

# xiaomin = Soldier('小明',2,2,'and')
# xiaohong = Soldier('小红',-4,4,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# xiaozhuang.update_target12(xiaomin,xiaohong)

# Soldier.Update_all_state()   ###################刚写的打包语句

# print(xiaozhuang.t1_to_s_ang)
# print(xiaozhuang.t2_to_s_ang)
# print(xiaozhuang.ang)
# for i in range(5000):
#     print(f'在{i}帧')

#     xiaozhuang.update_single_soldier()   ###################刚写的打包语句

#     if i == 10:
#         xiaohong.raise_flag = [1,True] #调试内容，小红在100帧举旗子，旗子上写的1
#     if i == 20:
#         xiaomin.raise_flag = [1,True] #调试内容，小明400帧举旗子，旗子上写的1
#     if xiaozhuang.remenber_1[1] and xiaozhuang.remenber_2[1]:
#         print('小壮正在思考')
#     if xiaozhuang.raise_flag[1]:
#         print(f'在{i}帧的时候，成功收集小红的{xiaozhuang.remenber_2[0]}，小明的{xiaozhuang.remenber_1[0]},并成功举旗为{xiaozhuang.raise_flag[0]}')
#         break

# # ==========================调试插排语句===================================

# from entities.soldier.soldier_generation import Soldier
# from math import *
# xiaomin = Soldier('小明',2,2,'and')
# xiaohong = Soldier('小红',-4,4,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# xiaohei = Soldier('小黑',7,10,'and')
# xiaobai = Soldier('小白',-3,-10,'nor')
# xiaolan = Soldier('小兰',-4,-3,'or')

# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaohei.update_target12(xiaohong,xiaozhuang)
# xiaobai.update_target12(xiaohei,xiaomin)
# xiaolan.update_target12(xiaobai,xiaohei)

# xiaomin.raise_flag = [1,True]   #预设啥子举旗
# xiaohong.raise_flag = [0,True]   #预设啥子举旗

# Soldier.Update_all_state()    #初始化

# for i in range(5000):    
#     # print(Soldier.All_soldier_t_3Dimformation())
#     Soldier.Update_all_t_state()
#     lis1 = Soldier.all_soldier_list
#     for s in lis1:
#         if s.level != 0:
#             if s.remenber_1[1] and s.remenber_2[1]:
#                 print(f'在{i}帧')
#                 print(f'{s.name}正在思考')
#             if s.raise_flag[1]:
#                 print(f'在{i}帧')
#                 print(f'在{i}帧的时候,逻辑门是{s.gate}{s.name}成功收集{s.target1.name}的{s.remenber_1[0]},{s.target2.name}的{s.remenber_2[0]}并成功举旗为{s.raise_flag[0]}')
#                 lis1.remove(s)
#                 if s.name == '小兰':
#                     break 
# # #==========================调试3d渲染初始化===================================
# import pyvista as pv
# from animation.soldier_3Dmodel import Soldier3D
# from entities.soldier.soldier_generation import Soldier
# from math import *

# xiaomin = Soldier('小明',5,5,'and')
# xiaohong = Soldier('小红',5,-5,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# xiaohei = Soldier('小黑',7,10,'and')
# xiaobai = Soldier('小白',-3,-10,'nor')
# xiaolan = Soldier('小兰',-4,-3,'or')

# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaohei.update_target12(xiaohong,xiaozhuang)
# xiaobai.update_target12(xiaohei,xiaomin)
# xiaolan.update_target12(xiaobai,xiaohei)

# xiaomin.raise_flag = [1,True]   #预设啥子举旗
# xiaohong.raise_flag = [0,True]   #预设啥子举旗

# Soldier.Update_all_state()    #初始化
# lis_3D = Soldier.All_soldier_t_3Dimformation()
# # print(lis_3D)

# plotter = pv.Plotter()
# plotter.set_background("white")
# plotter.add_axes()
# plotter.add_mesh(pv.Cube(center=(0, 0, 0), x_length=30, y_length=30, z_length=0.01), color="green")  #草坪
# Soldier3D.Init_soldier_lay_out(lis_3D,plotter)
# plotter.show()


# # #==========================调试3d渲染===================================
import sys
from PyQt5.QtWidgets import QApplication
from animation.scene3D import create_scene
from animation.main_window import MainWindow

from entities.soldier.soldier_generation import Soldier

from math import *


# xiaomin = Soldier('小明',5,5,'and')
# xiaohong = Soldier('小红',5,-5,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# xiaohei = Soldier('小黑',7,10,'and')
# xiaobai = Soldier('小白',-3,-10,'nor')
# xiaolan = Soldier('小兰',-4,-3,'or')

# xiaozhuang.update_target12(xiaomin,xiaohong)
# xiaohei.update_target12(xiaohong,xiaozhuang)
# xiaobai.update_target12(xiaohei,xiaomin)
# xiaolan.update_target12(xiaobai,xiaohei)

# xiaomin.raise_flag = [1,True]   #预设啥子举旗
# xiaohong.raise_flag = [0,True]   #预设啥子举旗



# 1. 创建Qt应用程序
app = QApplication(sys.argv)
# 2. 创建3D场景
plotter = create_scene()
# 5. 创建主窗口，把所有组件传入
window = MainWindow(plotter)
# 6. 显示窗口
window.show()
# 7. 启动程序循环
sys.exit(app.exec_())

# # #==========================调试举旗逻辑(似乎是对的)===================================

# from entities.soldier.soldier_generation import Soldier
# from math import *
# xiaomin = Soldier('小明',2,2,'and')
# xiaohong = Soldier('小红',-4,4,'or')
# xiaozhuang = Soldier('小壮',0,0,'and')
# # xiaohei = Soldier('小黑',7,10,'and')
# # xiaobai = Soldier('小白',-3,-10,'nor')
# # xiaolan = Soldier('小兰',-4,-3,'or')

# xiaozhuang.update_target12(xiaomin,xiaohong)
# # xiaohei.update_target12(xiaohong,xiaozhuang)
# # xiaobai.update_target12(xiaohei,xiaomin)
# # xiaolan.update_target12(xiaobai,xiaohei)

# xiaomin.raise_flag = [1,True]   #预设啥子举旗
# xiaohong.raise_flag = [0,True]   #预设啥子举旗

# Soldier.Update_all_state()    #初始化

# for i in range(5000):    
#     # print(Soldier.All_soldier_t_3Dimformation())
#     Soldier.Update_all_t_state()
#     if xiaozhuang.if_begin_raise_flag:
#         print(i)
#         print(f'剩余举起时间{xiaozhuang.t_raise_flag_time}')
#         print(xiaozhuang.raise_flag)