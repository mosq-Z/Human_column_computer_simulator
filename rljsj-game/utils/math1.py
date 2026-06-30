#一些要用到的简易运算
from math import *

# 距离计算
def distance(x1,y1,x2,y2):
    return  sqrt((x1-x2)**2 + (y1-y2)**2)

# 距离判定（偷个小懒算了）
def Distance_judgment(name1,vision1,x1,y1,name2,x2,y2):  #判定1的看2有没有超过1的视距
    ans = distance(x1,y1,x2,y2) <= vision1  #不超视距返回true
    if ans:
        print(f'士兵{name2}在士兵{name1}视距之中')
    else:
        print(f'士兵{name2}不在士兵{name1}视距之中哦！')
    return ans 

# 相对角度计算,返回两平面坐标相对角度，【0，pi）
def relative_angle(x1,y1,x2,y2):
    xx = x2 - x1
    yy = y2 - y1
    R = distance(x1,y1,x2,y2)
    ang = acos(xx/R)
    if yy<0:
        ang = 2*pi - ang
    # print(f'jiaodushi {ang}') 
    return ang

# 遮挡半角计算
def half_anglen(R,x1,y1):   # 被遮挡的半角,相对坐标
    d = distance(0,0,x1,y1) 
    sinn = R/d
    # print(f'sinn{sinn}  R{R}   d{d}')
    sigma = asin(sinn)
    return sigma

# 遮挡判定
def Occlusion_judgment(name1,x1,y1,name2,R2,x2,y2,name3,R3,x3,y3):  #判定1的看2的视野是否被3遮挡
    ang1to2 = relative_angle(x1,y1,x2,y2)
    ang1to3 = relative_angle(x1,y1,x3,y3)
    hfang1to2 = half_anglen(R2,x2-x1,y2-y1)
    hfang1to3 = half_anglen(R3,x3-x1,y3-y1)
    # print(ang1to2,ang1to3,hfang1to2,hfang1to3)
    l1t2 = ang1to2-hfang1to2
    r1t2 = ang1to2+hfang1to2
    l1t3 = ang1to3-hfang1to3
    r1t3 = ang1to3+hfang1to3
    # print(l1t2,r1t2,l1t3,r1t3)
    ans = not (l1t2 >= l1t3 and r1t2 <= r1t3)   # 未被遮挡返回True
    # if ans:
    #     print(f'{name1}观测{name2}的视野未被{name3}遮挡')
    # else:
    #     print(f'{name1}观测{name2}的视野被{name3}遮挡了哦！')
    return ans

