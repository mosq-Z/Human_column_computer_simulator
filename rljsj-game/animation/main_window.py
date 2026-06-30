from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer,Qt
from constants.game_config import basic_frame,total_frames
from entities.soldier.soldier_generation import Soldier
from animation.soldier_3Dmodel import Soldier3D
import pyvista as pv
import time



class MainWindow(QMainWindow):    #这是一个窗口父类
    def __init__(self, plotter):
        super().__init__()
        self.plotter = plotter       # 3D场景
        
        # 动画运行逻辑
        self.is_running = False  # 默认不动
        self.total_frames = total_frames  # 总动画帧数
        self.frame_cache = []    # 帧缓存列表
        self.current_frame_idx = 0  # 当前播放到第几帧
        
        
        # Soldier.Soldier_generation('小明',5,5,'and')
        # Soldier.Soldier_generation('小红',5,-5,'or')
        # Soldier.Soldier_generation('小壮',0,0,'and')
        # Soldier.Soldier_generation('小黑',7,10,'and')
        # Soldier.Soldier_generation('小白',-3,-10,'nor')
        # Soldier.Soldier_generation('小兰',-4,-3,'or')

        # Soldier.Raise_flag_by_name('小明',1)
        # Soldier.Raise_flag_by_name('小红',0)
        
        # Soldier.Change_target_by_name('小壮','小明','小红')
        # Soldier.Change_target_by_name('小黑','小红','小壮')
        # Soldier.Change_target_by_name('小白','小黑','小明')
        # Soldier.Change_target_by_name('小兰','小白','小黑')

        Soldier.Batch_identification_generation_of_soldiers()  #载入士兵文件,得到最大最小坐标
    
        # 设置窗口标题和大小
        self.setWindowTitle('亡灵大军计算机')
        self.setGeometry(100, 100, 1200, 800)
        self.build_ui()
        self.build_back_ground()

        # 初始化士兵位置
        self.soldier_lay_out()
        
        if self.soldier_Error():
            print('请根据提示调整士兵位置')
        else:
        # 启动定时器（驱动动画循环）
            self.pre_render_all_frames()  # 第一步：预计算所有帧
            self.start_timer()       # 第二步：启动播放定时器（只读缓存）
            pass

    

    # =====================================主窗口背景相机构建函数==================================
    def build_back_ground(self):
        # 设置背景颜色为白色,好像默认就是白色
        self.plotter.set_background("white")
        # 显示坐标轴（方便看方向）,神秘草坪
        self.plotter.add_axes()
        xm = Soldier.x_min
        ym = Soldier.y_min
        xc = (Soldier.x_min + Soldier.x_max)/2
        yc = (Soldier.y_min + Soldier.y_max)/2
        xl = - Soldier.x_min + Soldier.x_max +3
        yl = - Soldier.y_min + Soldier.y_max +3
        print(f'xc,yc,xl,yl{xc,yc,xl,yl}')
        self.plotter.add_mesh(pv.Cube(center=(xc,yc, 0), x_length=xl, y_length=yl, z_length=0.1), color="green")  #草坪
        self.plotter.camera_position = [(xm-5, ym-5, (xl+yl)/2), (xc, yc, 0),(0, 0, 1)]
    # =====================================主窗口背景构建函数==================================


    # =====================================按钮及UI布局函数==================================
    # 这部分代码控制按钮排布和按钮逻辑

    # 按钮创建和排列
    def build_ui(self):
        # 创建三个按钮
        self.start_btn = QPushButton("开始模拟")
        self.pause_btn = QPushButton("暂停模拟")
        # self.reset_btn = QPushButton("重置位置")
        # self.generate_btn = QPushButton('新建士兵')
        # self.revise_btn = QPushButton('修改士兵')
        layout = QVBoxLayout()  # 主布局：垂直布局（上面3D画面，下面按钮）
        layout.addWidget(self.plotter)  # 把3D画布添加到主布局
        
        # 按钮横向布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        # btn_layout.addWidget(self.reset_btn)
        # btn_layout.addWidget(self.generate_btn)
        # btn_layout.addWidget(self.revise_btn)


        layout.addLayout(btn_layout)# 把按钮布局加到主布局
        
        # 设置中心容器
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # 按钮绑定功能（点击后执行对应函数）
        self.start_btn.clicked.connect(self.start_simulation)
        self.pause_btn.clicked.connect(self.pause_simulation)
        # self.reset_btn.clicked.connect(self.reset_simulation)
        # self.generate_btn.clicked.connect(self.generate_soldier)
        # self.revise_btn.clicked.connect(self.revise_soldier)

    # ---------------------- 按钮功能函数 ----------------------
    def start_simulation(self):
        self.is_running = True
        print('按下开始按钮')
        
    def pause_simulation(self):
        self.is_running = False

    # def reset_simulation(self):
    #     self.is_running = False  #停止模拟
    #     self.plotter.clear()
    #     self.build_back_ground()
    #     self.soldier_lay_out()   #初始化士兵并构建3D模型

    # def generate_soldier(self):
    #     text, ok = QInputDialog.getText(self, "创建士兵", "请输入：姓名 x y 逻辑门（用空格分隔）")
    #     if not ok:  # 用户点取消
    #         return
        
    #     # 2. 分割并校验输入
    #     parts = text.split()
    #     if len(parts) != 4:
    #         QMessageBox.warning(self, "输入错误", "请输入 4 个值：姓名 x y 逻辑门")
    #         return
    #     name, x_str, y_str, gate = parts
        
    #     # 3. 尝试转换坐标为数字
    #     try:
    #         x = float(x_str)
    #         y = float(y_str)
    #     except ValueError:
    #         QMessageBox.warning(self, "输入错误", "x/y 必须是数字")
    #         return
        
    #     # 4. 创建士兵并更新布局
    #     Soldier.Soldier_generation(name, x, y, gate)
    #     self.soldier_lay_out()    
        
        
    # def revise_soldier(self):
    #     text, ok = QInputDialog.getText(self, "修改士兵", "请输入：姓名")
    #     if not ok: 
    #         return

    #     s = Soldier.Find_sol_by_name(text)
    #     if s == None :
    #         QMessageBox.warning(self, "输入错误", "未找到对应士兵")
    #         return
    #     else:
    #         text2, ok = QInputDialog.getText(self, "修改士兵", "请输入：mb 目标1姓名 目标2姓名 /ss 始终输出（中间用空格分隔）")
    #         parts = text2.split()
    #         if len(parts) != 2 and len(parts) != 3:
    #             QMessageBox.warning(self, "输入错误", "请按照要求输入")
    #             return
    #         else:
    #             if parts[0] == 'mb':
    #                 s1 = Soldier.Find_sol_by_name(parts[1])        
    #                 s2 = Soldier.Find_sol_by_name(parts[2])
    #                 if s1 == s2 == None:
    #                     QMessageBox.warning(self, "输入错误", "未找到对应士兵")
    #                     return
    #                 else:
    #                     Soldier.Change_target_by_name(text,parts[1],parts[2])
    #                     self.plotter.clear()
    #                     self.build_back_ground()
    #                     self.soldier_lay_out()     

    #             elif parts[0] == 'ss':
    #                 try:
    #                     x = int(parts[1])
    #                 except ValueError:
    #                     QMessageBox.warning(self, "输入错误", " 输入必须是0/1")
    #                     return
    #                 Soldier.Raise_flag_by_name(text,parts[1])
    #                 self.plotter.clear()
    #                 self.build_back_ground()
    #                 self.soldier_lay_out()   

    #             else:
    #                 QMessageBox.warning(self, "输入错误", "非法标识，请重新输入")
    #                 return











    
    # =====================================时钟与帧更新==================================

    # 初始化士兵位置函数,并渲染
    def soldier_lay_out(self):
        if len(Soldier.all_soldier_list) > 0:
            Soldier.Update_all_state()
            lis_3D = Soldier.All_soldier_t_3Dimformation()
            Soldier3D.Init_soldier_lay_out(lis_3D,self.plotter)    #构建 
            self.plotter.update() #这个是内置函数
    
    # 士兵位置不合理报警
    def soldier_Error(self):
        return not Soldier.all_soldier_already

    # PyQt5的内置帧函数，可以放进我预设的帧时长,每执行一次update_frame函数
    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_play_timer)
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.start(int(basic_frame*1000))

    # 预计算所有帧
    def pre_render_all_frames(self):
        for f in range(self.total_frames):
            Soldier.Update_all_t_state()
            lis_3D = Soldier.All_soldier_t_3Dimformation()
            self.frame_cache.append(lis_3D)
            
            if f%10 == 0:
                print(f'已经加载到{f}帧')
        print(f'已经所有帧的加载，列表长度为{len(self.frame_cache)}，可以播放动画')


    # 启动定时播放器
    def start_play_timer(self):
        if self.is_running:

            t0 = time.perf_counter()

            frame_now = self.frame_cache[self.current_frame_idx]

            t1 = time.perf_counter()

            Soldier3D.Update_soldier_lay_out(frame_now,Soldier.all_Soldier_flag_time,basic_frame)

            t2 = time.perf_counter()

            self.plotter.update() #这个是内置函数
            # print (f'正在播放{self.current_frame_idx}帧')
            self.current_frame_idx  = self.current_frame_idx +1
            if self.current_frame_idx == self.total_frames :
                self.is_running = False
                print("动画播放完成")

        
            t3 = time.perf_counter()

            print(f"总共:{(t3-t0)*1000:.1f} | "
                f"更新:{(t2-t1)*1000:.1f} | "
                f"渲染:{(t3-t2)*1000:.1f} ms")        
        else:
            pass
    

