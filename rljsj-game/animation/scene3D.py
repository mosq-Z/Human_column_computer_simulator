from pyvistaqt import QtInteractor
import pyvista as pv
def create_scene():
    """
    创建并返回一个3D场景————豆包抄来的，方便后面编写UI的时候引入按钮元素
    """
    # 创建3D渲染器（嵌入Qt窗口）
    plotter = QtInteractor()
    # # 设置背景颜色为白色,好像默认就是白色
    # plotter.set_background("white")
    # # 显示坐标轴（方便看方向）,神秘草坪
    # plotter.add_axes()
    # plotter.add_mesh(pv.Cube(center=(0, 0, 0), x_length=10, y_length=10, z_length=0.01), color="green")  #草坪

    return plotter