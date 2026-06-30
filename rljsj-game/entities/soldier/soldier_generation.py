from .soldier_constants import Soldier_vision,Soldier_volume,Soldier_turning_time,Soldier_thinking_time,Soldier_flag_time
from .soldier_calculations import gate_calculation,turning_time_calculation,ang_calculation,all_Occlusion_judgment,all_Distance_judgment,all_overlap_judgement,update_receive,update_remenber,update_ang,update_lev
from constants.game_config import basic_frame
from utils.math1 import relative_angle

#士兵的生成，现在xy上放置士兵‘大壮’，他的逻辑门是
class Soldier:

    all_soldier_list = []  #存储每一个生成的士兵
    all_soldier_already = True #所有士兵均已准备好，无视野视距碰撞箱问题
    all_Soldier_flag_time = Soldier_flag_time  #为了引用方便写的，其实下面不少实例变量可以写成类变量的，但是写的时候还没见过类变量
    x_max = x_min = y_max = y_min = 0  #类变量记录最大最小


    def __init__(self,name,x,y,gate):
        # 基础属性：名字，位置，逻辑门
        self.name = name
        self.x = x
        self.y = y
        self.gate = gate
        
        # 交互属性：目标1，目标2，所属层级
        self.target1 = None
        self.target2 = None
        self.level = 0
        
        # 预设属性：思考时间，持续举旗时间,视野半径,碰撞箱半径，转向延迟
        self.thinking_time = Soldier_thinking_time
        self.vision = Soldier_vision
        self.radius = Soldier_volume
        self.turning_per_time = Soldier_turning_time
        self.raise_flag_time = Soldier_flag_time
        
        # 静态属性(初始化值)：居中视角，转向时间，是否看得到目标1，是否看得到目标2
        self.ang = 0.0
        self.turning_time = 0.0
        self.t1_to_s_ang = 0.0
        self.t2_to_s_ang = 0.0
        self.if_1_invision = False
        self.if_2_invision = False
        self.if_overlap = False

        # 动态属性（帧运算参数）:按照帧时长计算的视野张角，t时刻的视角，
                                # t时刻转头方向（1逆时针，-1顺时针，0不转），是否接受到1的信号，是否接受到2的信号，
                                # 是否记忆1的信号【内容，是否】，是否记忆2的信号【内容，是否】，是否完成举旗【内容，是否】
                                # t时刻剩余思考时间,t时刻剩余举旗时间，是否开始举旗
        self.field_of_view_ang = 1/self.turning_per_time * basic_frame
        self.t_ang = 0.0
        self.pre_t_ang = 0.0   #保存这一帧所在角度
        self.t_t_direc = 1
        self.receive_from_1 = False
        self.receive_from_2 = False
        self.remenber_1 = [None,False]
        self.remenber_2 = [None,False]
        self.raise_flag = [None,False]
        self.t_thkig_time = self.thinking_time
        self.t_raise_flag_time = self.raise_flag_time
        self.if_begin_raise_flag = False

        # 更新类变量
        Soldier.all_soldier_list.append(self)
        print(f'已在（{self.x}，{self.y}）添加士兵{self.name}，逻辑门为{self.gate}')

    # ================================================初始化状态函数================================================
    # 这个部分负责更新士兵的初始状态

    # 设定目标-------这个最好写一个输入语句
    def update_target12(self,tg1,tg2):
        self.target1 = tg1
        self.target2 = tg2
        if self.target1 != None and self.target2 != None:
            print (f'已把士兵{self.name}的目标1修改为{tg1.name},目标2修改为{tg2.name}')
        elif self.target1 != None and self.target2 == None:
            print (f'已把士兵{self.name}的目标1修改为{tg1.name},目标2未指定')
    
    # 更新层级，排列层级
    def update_level(self):
        self.level = update_lev(self,0)
        print (f'士兵{self.name}的层级是{self.level}')
    @classmethod
    def update_all_level(cls):
        for i in cls.all_soldier_list:
            i.update_level()
    @classmethod
    def Sort_all_soldier_list(cls):
        sorted_lis = [cls.all_soldier_list[0]]
        for s in cls.all_soldier_list[1:]:
            i = 0
            while True:
                if i == len(sorted_lis)-1 or sorted_lis[i].level >= s.level:
                    break
                else:
                    i+=1
            sorted_lis.insert(i+1,s)
        # for i in sorted_lis:
        #     print(i.level)
        cls.all_soldier_list = sorted_lis

    # 更新居中视角（同时初始化0时刻的视角）
    def update_ang(self):
        if self.target1 != None and self.target2 != None:
            self.ang = self.t_ang = self.pre_t_ang = ang_calculation(self.x,self.y,\
                                    self.target1.x,self.target1.y,\
                                    self.target2.x,self.target2.y)
            print (f'士兵{self.name}观察居中视角是{self.ang:.2f}')
        elif self.target1 != None and self.target2 == None:
            self.ang = self.t_ang = self.pre_t_ang = self.t1_to_s_ang = self.t2_to_s_ang = relative_angle(self.x,self.y,self.target1.x,self.target1.y)
            #固定这个角度即可,这个士兵的所有角度固定即可
            print (f'士兵{self.name}观察居中视角是{self.ang:.2f}')
        else :
            print (f'士兵{self.name}观察居中视角是{self.ang:.2f}')
            #啥也不看，所有角度参数均为默认值
    @classmethod
    def update_all_ang(cls):
        for i in cls.all_soldier_list:
            i.update_ang()
    
    # 更新转向时间(同时更新目标12相对士兵角度)
    def update_turning_time(self):
        if self.target1 != None and self.target2 != None:
            Ans = turning_time_calculation(self.x,self.y,\
                                            self.target1.x,self.target1.y,\
                                            self.target2.x,self.target2.y,\
                                            self.turning_per_time)
            self.turning_time = Ans[0]
            self.t1_to_s_ang = Ans[1]
            self.t2_to_s_ang = Ans[2]
            print (f'士兵{self.name}观察需要时间是{self.turning_time:.2f}')
        else:
            print (f'士兵{self.name}观察需要时间是{self.turning_time:.2f}') #剩余两个参数在更新居中视角函数里面就更新过了
    @classmethod
    def update_all_turning_time(cls):
        for i in cls.all_soldier_list:
            i.update_turning_time()
    
    # 更新观测状态
    def update_if_12_invision(self):
        # print(f'Soldier.all_soldier_list{Soldier.all_soldier_list}')
        if self.target1 != None:
            S_a1 = Soldier.all_soldier_list
            A1 = all_Occlusion_judgment(self,self.target1,S_a1)
            B1 = all_Distance_judgment(self,self.target1)
            self.if_1_invision = A1 and B1
            if not(A1 and B1):
                Soldier.all_soldier_already = False  #报错修改类标签
        if self.target2 != None:
            S_a2 = Soldier.all_soldier_list
            A2 = all_Occlusion_judgment(self,self.target2,S_a2)
            B2 = all_Distance_judgment(self,self.target2)
            self.if_2_invision = A2 and B2
            if not(A2 and B2):
                Soldier.all_soldier_already = False  #报错修改类标签
    @classmethod
    def update_all_if_12_invision(cls):
        for i in cls.all_soldier_list:
            i.update_if_12_invision()

    # 更新重合状态
    def update_if_overlap(self):
        S_a = Soldier.all_soldier_list
        self.if_overlap = all_overlap_judgement(self,S_a,self.radius)
        if not self.if_overlap:
            Soldier.all_soldier_already = False  #报错修改类标签
    @classmethod
    def update_all_if_overlap(cls):
        for i in cls.all_soldier_list:
            i.update_if_overlap()
    
    # 状态打印
    def information(self):
        print('============================')
        print (f'长官好!一下是我的个人信息：\n我的名字是{self.name}；\n我的坐标是（{self.x}，{self.y}）；\n我执行的运算是{self.gate}；\n我目前朝向{self.ang}弧度；\n转向用时是{self.turning_time}；')

        if  self.target1 != None:
            
            if self.if_1_invision == True:
                print(f'目前可以看到{self.target1.name}；')
            else:
                print(f'目前看不到{self.target1.name}；')
        else :
            print('我没有被指派观察目标1')

        if  self.target2 != None:
            if self.if_2_invision == True:
                print(f'目前可以看到{self.target2.name}；')
            else:
                print(f'目前看不到{self.target2.name}；')
        else :
            print('我没有被指派观察目标2')

        print('============================')
    # ================================================初始化状态函数================================================



    # ================================================帧操作函数================================================
    # 这个部分负责处理在每一帧中士兵的状态更新和相关判定

    # 更新是否接受到1的信号，是否接受到2的信号
    def update_receive_from_1_or_2(self):
        if self.target1 != None:
            self.receive_from_1 = update_receive(self.t1_to_s_ang,self.t_ang,self.field_of_view_ang)
        if self.target2 != None:
            self.receive_from_2 = update_receive(self.t2_to_s_ang,self.t_ang,self.field_of_view_ang)
    
    # 更新记忆1的信号内容，记忆2的信号内容
    def update_remenber_1_or_2(self):
        if self.target1 != None:
            self.remenber_1 = update_remenber(self.remenber_1,self.remenber_1[1],self.receive_from_1,self.target1.raise_flag[1],self.target1.raise_flag[0])
        else:
            self.remenber_1 = [None,True]  #直接产生一个虚假的记忆
        if self.target2 != None:
            self.remenber_2 = update_remenber(self.remenber_2,self.remenber_2[1],self.receive_from_2,self.target2.raise_flag[1],self.target2.raise_flag[0])
        else:
            self.remenber_2 = [None,True]  #直接产生一个虚假的记忆

    # 更新下一帧的角度
    def update_t_ang(self):
        # print(f'士兵{self.name}的角度和方向分别是{self.t_ang},{self.t_t_direc}')
        if self.target1 != None and self.target2 != None:
            v = 1/self.turning_per_time
            self.t_ang,self.t_t_direc = update_ang(basic_frame,v,self.t_ang,self.t_t_direc,self.receive_from_1,self.receive_from_2,self.remenber_1[1],self.remenber_2[1])
        else :
            pass  #单一输入的哥们一直看着一个地方就好了

    # 更新下一帧思维状态(剩余思考时间)与是否开始举旗
    def update_t_thkig_time(self):
        if self.remenber_1[1] and self.remenber_2[1] and self.t_thkig_time > 0 and not self.if_begin_raise_flag:
            self.t_thkig_time -= basic_frame
        if self.t_thkig_time <= 0:
            self.if_begin_raise_flag = True
    
    # 更新举旗计算内容
    def update_raise_flag(self):
        if self.if_begin_raise_flag:
            ans = gate_calculation(self.gate,self.remenber_1[0],self.remenber_2[0])
            self.raise_flag = [ans,self.raise_flag[1]]
    
    # 更新下一帧举旗剩余时间
    def update_t_raise_flag_time(self):
        if self.if_begin_raise_flag and self.t_raise_flag_time > 0 :
            self.t_raise_flag_time -= basic_frame
            # print(self.t_raise_flag_time)
        if self.t_raise_flag_time <= 0:
            self.raise_flag = [self.raise_flag[0],True]
            self.if_begin_raise_flag = False
    
    # 单个士兵的帧操作打包
    def update_single_soldier(self):
        self.update_receive_from_1_or_2() #接收
        self.update_remenber_1_or_2() #记忆
        self.update_t_thkig_time() #思考
        self.update_raise_flag() #输出
        self.update_t_raise_flag_time()#举旗延迟
        self.pre_t_ang = self.t_ang
        self.update_t_ang() #转头

    # 单个士兵的帧操作————》3D动画需要的参数（士兵姓名（可能以后当编号来用），士兵坐标，士兵身体角度，此帧头角度，举旗状态，是否有举旗动作）
    def single_soldier_3Dimformation(self):
        return [self.name,self.x,self.y,self.ang,self.pre_t_ang,self.raise_flag,self.if_begin_raise_flag]

    # ================================================帧操作函数================================================

    

    # ================================================批量操纵类函数================================================
    # 这个部分整合士兵操作，方便对接到动画模块和玩家的输入

    # 在设定所有士兵目标后初始化所有状态函数（包括层级）
    @classmethod
    def Update_all_state(cls):
        Soldier.update_all_level()
        Soldier.update_all_ang()
        Soldier.update_all_turning_time()
        Soldier.update_all_if_12_invision()
        Soldier.update_all_if_overlap()
        Soldier.Sort_all_soldier_list()
        if Soldier.all_soldier_already:
            print(f'所有士兵的状态均无异常')
        else :
            print(f'有士兵的状态存在异常')
    
    # 按照层级大小逐个更新每个士兵的帧操作
    @classmethod
    def Update_all_t_state(cls):
        for s in cls.all_soldier_list:
            if s.level != 0:   #零层的啥子不需要操作
                s.update_single_soldier()

    # 生成这一帧每一个士兵的3D信息：姓名，此帧头角度，举旗状态
    @classmethod
    def All_soldier_t_3Dimformation(cls):
        lis_3D = [] 
        for s in cls.all_soldier_list:
            lis_3D.append(s.single_soldier_3Dimformation())
        return lis_3D

    # ================================================批量操纵类函数================================================

    # ================================================士兵生成与修改类函数================================================
    
    # 根据提供的姓名，坐标，逻辑门生成一个实例
    @classmethod
    def Soldier_generation(cls,name,x,y,gate):
        sol  = cls(name,x,y,gate)
    
    # 根据实例的姓名，找到这个实例
    @classmethod
    def Find_sol_by_name(cls,name):
        for s in cls.all_soldier_list:
            if s.name == name:
                return s
        return None
            
    # 根据提供的姓名,修改始终举旗信息,顺手取消掉他的两个目标
    @classmethod
    def Raise_flag_by_name(cls,name,flag):
        s = cls.Find_sol_by_name(name)
        s.raise_flag = [flag,True]
        s.target1 = None
        s.target2 = None

    # 根据提供的姓名俩目标的姓名，修改目标
    @classmethod
    def Change_target_by_name(cls,name,target1,target2):
        s = cls.Find_sol_by_name(name)
        if target1 != None and target2 != None:
            t1 = cls.Find_sol_by_name(target1)
            t2 = cls.Find_sol_by_name(target2)
            s.target1 = t1
            s.target2 = t2
        elif target1 == None and target2 != None:
            t1 = cls.Find_sol_by_name(target2)
        elif target2 == None and target1 != None:
            t1 = cls.Find_sol_by_name(target1)
        else:
            pass
    
    # 根据提供的姓名删除一个实例
    @classmethod
    def delete_sol_by_name(cls,name):
        lis = cls.all_soldier_list
        for s in range(len(cls.all_soldier_list)):
            if cls.all_soldier_list[s].name == name:
                cls.all_soldier_list = lis[0:s] + lis[s+1:]
                break
    
    # 士兵的批量识别生成
    @classmethod
    def Batch_identification_generation_of_soldiers(cls):
        filename="soldiers.txt"

        x_max1 = -float('inf')
        x_min1 = float('inf')
        y_max1 = -float('inf')
        y_min1 = float('inf')
        #读取的时候顺便记录一下边界，方便绘制地图和视角

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                # 去掉空行、空格、换行
                line = line.strip()
                if not line or line[0] == '#': #设置一些注释
                    continue
                parts = line.split()
                
                
                # 必须是 4 个数据：名字 x y 逻辑门
                if len(parts) == 4:
                    name = parts[0]
                    x = float(parts[1])
                    y = float(parts[2])
                    gate = parts[3]
                    cls.Soldier_generation(name,x,y,gate)

                    x_max1 = max(x_max1,x)
                    x_min1 = min(x_min1,x)
                    y_max1 = max(y_max1,y)
                    y_min1 = min(y_min1,y)

                elif len(parts) == 3:
                    name = parts[0]
                    target1 = parts[1]
                    target2 = parts[2]
                    cls.Change_target_by_name(name,target1,target2)

                elif len(parts) == 2:
                    name = parts[0]
                    flag = int(parts[1])
                    cls.Raise_flag_by_name(name,flag)

                else:
                    pass


        if x_max1 == -float('inf'):  # 说明没有读取到任何士兵坐标
            x_min1, x_max1 = -25, 25
            y_min1, y_max1 = -25, 25

        cls.x_min = x_min1
        cls.y_min = y_min1
        cls.x_max = x_max1
        cls.y_max = y_max1
        print(f'x_min1,y_min1,x_max1,y_max1{x_min1,y_min1,x_max1,y_max1}')
        
            































    # 重置状态






















    # def update_receive_from_1(self):
    # def update_receive_from_2(self):
    # def update_remenber_1(self):
    # def update_remenber_2(self):
    # def update_raise_flag(self)

    


