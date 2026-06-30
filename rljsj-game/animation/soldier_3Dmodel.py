# import pyvista as pv
# from math import *


# class Soldier3D:

#     all_soldier3D_list = []  #存储每一个生成的士兵3D模型

#     def __init__(self, plotter):
#         self.plotter = plotter
#         self.create_model()
#         self.loc = (0,0,0)  #当前整体坐标：控制旋转的相对位置，我真是天才
#         self.current_angle = 0.0 #当前头部视角：控制头部旋转为绝对旋转    此处左右角度均不是弧度
        
#         # 更新类变量
#         Soldier3D.all_soldier3D_list.append(self)

#     # ================================================单个士兵模型构造函数================================================
#     # 模型生成
#     def create_model(self):
#         # 创建身体：躯干，头，手臂*2,眼睛
#         self.body = pv.Cube(center=(0, 0, 1), x_length=1, y_length=1, z_length=2)
#         self.plotter.add_mesh(self.body, color="skyblue")

#         # 眼睛作为头的子结构(失败了)
#         self.head = pv.Cube(center=(0, 0, 1+1+0.5), x_length=0.8, y_length=0.8, z_length=0.8)
#         self.eye1 = pv.Sphere(center=( 0.4,-0.3, 1+1+0.5), radius=0.125)
#         self.eye2 = pv.Sphere(center=( 0.4,0.3, 1+1+0.5), radius=0.125)
#         self.plotter.add_mesh(self.head, color="skyblue")
#         self.plotter.add_mesh(self.eye1, color="white")
#         self.plotter.add_mesh(self.eye2, color="white")

#         # 手臂部分
#         self.arm1 = pv.Cube(center=( 0,-0.75, 1.25), x_length=0.5, y_length=0.5, z_length=1)
#         self.arm2 = pv.Cube(center=( 0,0.75, 1.25), x_length=0.5, y_length=0.5, z_length=1)
#         self.plotter.add_mesh(self.arm1, color="white")
#         self.plotter.add_mesh(self.arm2, color="red")

#     #  位置设定(相对)
#     def set_pos(self, x, y):
#         self.body.translate([x, y, 0], inplace=True)
#         self.head.translate([x, y, 0], inplace=True)
#         self.arm1.translate([x, y, 0], inplace=True)
#         self.arm2.translate([x, y, 0], inplace=True)
#         self.eye1.translate([x, y, 0], inplace=True)
#         self.eye2.translate([x, y, 0], inplace=True)
#         self.loc =(x,y,0)

#     # 全身角度（相对）
#     def set_ang(self,ang):
#         self.body.rotate_z(ang,point=self.loc,inplace=True)
#         self.head.rotate_z(ang,point=self.loc,inplace=True)
#         self.arm1.rotate_z(ang,point=self.loc,inplace=True)
#         self.arm2.rotate_z(ang,point=self.loc,inplace=True)
#         self.eye1.rotate_z(ang,point=self.loc,inplace=True)
#         self.eye2.rotate_z(ang,point=self.loc,inplace=True)
#         self.current_angle = ang

#     # 头部角度（**绝对**）
#     def set_t_ang(self,t_ang):
#         self.head.rotate_z(-self.current_angle, point=self.loc, inplace=True)
#         self.head.rotate_z(t_ang,point=self.loc,inplace=True)
#         self.eye1.rotate_z(-self.current_angle, point=self.loc, inplace=True)
#         self.eye1.rotate_z(t_ang,point=self.loc,inplace=True)
#         self.eye2.rotate_z(-self.current_angle, point=self.loc, inplace=True)
#         self.eye2.rotate_z(t_ang,point=self.loc,inplace=True)
#         self.current_angle = t_ang

#     # 初始举白旗/黑旗（相对）
#     def set_flag1(self):
#         self.arm1.translate([0, 0, 1.2], inplace=True)
#     def set_flag2(self):
#         self.arm2.translate([0, 0, 1.2], inplace=True)
    
#     # 逐渐举白旗/黑旗（相对）(参数是举旗的总时长和一帧的时长)
#     def set_t_flag1(self,Soldier_flag_time,basic_frame):
#         self.arm1.translate([0, 0, 1.2/(Soldier_flag_time/basic_frame)], inplace=True)
#     def set_t_flag2(self,Soldier_flag_time,basic_frame):
#         self.arm2.translate([0, 0, 1.2/(Soldier_flag_time/basic_frame)], inplace=True)


#     # 显示士兵名字
#     def set_name(self,name):
#         x, y, z = self.loc
#         points = [(x, y, z + 3.5)]  # 头顶位置
#         labels = [name]
#         self.plotter.add_point_labels(
#             points,
#             labels,
#             font_size=14,
#             text_color="yellow",
#             point_size=0  # 隐藏点本身，只显示文字
#         )
    
#     # ================================================单个士兵模型生成函数================================================
    

#     # ================================================批量士兵模型生成函数================================================
    
#     # 士兵3D模型初始化:按照士兵逻辑类提供的信息，批量渲染士兵
#     @classmethod
#     def Init_soldier_lay_out(cls,lis_3D,plotter):
        
#         for s_inf in lis_3D :
#             # print("当前士兵数据：", s_inf, "长度：", len(s_inf))
#             soldier_x = cls(plotter)
#             soldier_x.set_pos(s_inf[1],s_inf[2])
#             soldier_x.set_ang(degrees(s_inf[3]))
#             # print(degrees(s_inf[3]))
#             soldier_x.set_t_ang(degrees(s_inf[4]))
#             if s_inf[5][1] :
#                 if s_inf[5][0] == 1:
#                     soldier_x.set_flag1()
#                 else :
#                     soldier_x.set_flag2()
#             soldier_x.set_name(s_inf[0])

#     @classmethod
#     def Update_soldier_lay_out(cls,lis_3D,Soldier_flag_time,basic_frame):
#         for i in range(len(cls.all_soldier3D_list)):
#             soldier_x = cls.all_soldier3D_list[i]
#             s_inf  = lis_3D[i]
#             soldier_x.set_t_ang(degrees(s_inf[4]))
#             if s_inf[6] :
#                 if s_inf[5][0] == 1:
#                     soldier_x.set_t_flag1(Soldier_flag_time,basic_frame)
#                 else :
#                     soldier_x.set_t_flag2(Soldier_flag_time,basic_frame)

        


# # plotter = pv.Plotter()
# # plotter.set_background("white")
# # plotter.add_mesh(pv.Cube(center=(0, 0, 0), x_length=10, y_length=10, z_length=0.01), color="green")  #草坪
# # soldier1 = Soldier3D(plotter)
# # soldier2 = Soldier3D(plotter)
# # plotter.show()


#豆包爹太牛逼了，真遭不住，写的太好了太艺术了，我真的来不及了，上面的自己写的建模一次就要400ms多，豆包爹写的0.1ms
import pyvista as pv
from math import *

class Soldier3D:
    all_soldier3D_list = []

    def __init__(self, plotter):
        self.plotter = plotter
        self.create_model()

        self.loc = (0, 0, 0)
        self.current_angle = 0.0
        self.head_abs_angle = 0.0

        # 举旗状态
        self.arm1_lift = 0.0
        self.arm2_lift = 0.0

        Soldier3D.all_soldier3D_list.append(self)

    # ================================================
    # 【极速版模型创建：只创建一次，保存 ACTORS】
    # ================================================
    def create_model(self):
        # 身体
        self.body = self.plotter.add_mesh(
            pv.Cube(center=(0, 0, 1), x_length=1, y_length=1, z_length=2),
            color="skyblue", pickable=False
        )

        # 头 + 眼睛
        self.head = self.plotter.add_mesh(
            pv.Cube(center=(0, 0, 2.5), x_length=0.8, y_length=0.8, z_length=0.8),
            color="skyblue", pickable=False
        )
        self.eye1 = self.plotter.add_mesh(
            pv.Sphere(center=(0.4, -0.3, 2.5), radius=0.125),
            color="white", pickable=False
        )
        self.eye2 = self.plotter.add_mesh(
            pv.Sphere(center=(0.4, 0.3, 2.5), radius=0.125),
            color="white", pickable=False
        )

        # 手臂
        self.arm1 = self.plotter.add_mesh(
            pv.Cube(center=(0, -0.75, 1.25), x_length=0.5, y_length=0.5, z_length=1),
            color="white", pickable=False
        )
        self.arm2 = self.plotter.add_mesh(
            pv.Cube(center=(0, 0.75, 1.25), x_length=0.5, y_length=0.5, z_length=1),
            color="red", pickable=False
        )

    # ================================================
    # 【极速：设置位置 → 显卡级别的 SetPosition】
    # ================================================
    def set_pos(self, x, y):
        self.loc = (x, y, 0)
        for actor in [self.body, self.head, self.eye1, self.eye2, self.arm1, self.arm2]:
            actor.SetPosition(x, y, 0)

    # ================================================
    # 【极速：全身旋转 → 显卡旋转】
    # ================================================
    def set_ang(self, ang):
        for actor in [self.body, self.head, self.eye1, self.eye2, self.arm1, self.arm2]:
            actor.SetOrientation(0, 0, ang)
        self.current_angle = ang

    # ================================================
    # 【极速：头部绝对旋转 → 不再反复旋转！】
    # ================================================
    def set_t_ang(self, t_ang):
        self.head.SetOrientation(0, 0, t_ang)
        self.eye1.SetOrientation(0, 0, t_ang)
        self.eye2.SetOrientation(0, 0, t_ang)
        self.head_abs_angle = t_ang

    # ================================================
    # 【极速：举旗 → 直接 SetPosition，不修改顶点】
    # ================================================
    def set_flag1(self):
        self.arm1_lift = 1.2
        self.arm1.SetPosition(self.loc[0], self.loc[1],  1.2)

    def set_flag2(self):
        self.arm2_lift = 1.2
        self.arm2.SetPosition(self.loc[0], self.loc[1],  1.2)

    def set_t_flag1(self, Soldier_flag_time, basic_frame):
        step = 1.2 / (Soldier_flag_time / basic_frame)
        self.arm1_lift += step
        self.arm1.SetPosition(self.loc[0], self.loc[1],  self.arm1_lift)

    def set_t_flag2(self, Soldier_flag_time, basic_frame):
        step = 1.2 / (Soldier_flag_time / basic_frame)
        self.arm2_lift += step
        self.arm2.SetPosition(self.loc[0], self.loc[1],  self.arm2_lift)

    # ================================================
    # 名字只创建一次，不重复创建
    # ================================================
    def set_name(self, name):
        x, y, z = self.loc
        self.plotter.add_point_labels(
            [(x, y, z + 3.5)], [name],
            font_size=7, text_color="yellow", point_size=0
        )

    # ================================================
    # 以下完全不用改
    # ================================================
    @classmethod
    def Init_soldier_lay_out(cls, lis_3D, plotter):
        for s_inf in lis_3D:
            soldier_x = cls(plotter)
            soldier_x.set_pos(s_inf[1], s_inf[2])
            soldier_x.set_ang(degrees(s_inf[3]))
            soldier_x.set_t_ang(degrees(s_inf[4]))
            if s_inf[5][1]:
                if s_inf[5][0] == 1:
                    soldier_x.set_flag1()
                else:
                    soldier_x.set_flag2()
            soldier_x.set_name(s_inf[0])

    @classmethod
    def Update_soldier_lay_out(cls, lis_3D, Soldier_flag_time, basic_frame):
        for i in range(len(cls.all_soldier3D_list)):
            soldier_x = cls.all_soldier3D_list[i]
            s_inf = lis_3D[i]
            soldier_x.set_t_ang(degrees(s_inf[4]))
            if s_inf[6]:
                if s_inf[5][0] == 1:
                    soldier_x.set_t_flag1(Soldier_flag_time, basic_frame)
                else:
                    soldier_x.set_t_flag2(Soldier_flag_time, basic_frame)