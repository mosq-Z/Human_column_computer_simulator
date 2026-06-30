from math import*
#输入一个逻辑门名字和两个输入，返回对应输出
def gate_calculation(name,input1,input2):   
    LG = {
        'buf':input1,
        'not':not input1,
        'and':input1 and input2,
        'or':input1 or input2,
        'nand':not (input1 and input2),
        'nor':not (input1 or input2),
        'xor':input1 and not input2 or not input1 and input2,
        'xnor':input1 and input2 or not input1 and not input2
    }
    if name in LG.keys():
        # print('识别逻辑门成功')
        return LG[name]
        
    else:
        print('无效逻辑门')
        return 10086

#输入123三个士兵的位置，1的转向速度，计算夹角并返回转向延迟
from utils.math1 import relative_angle
def turning_time_calculation(x1,y1,x2,y2,x3,y3,v):
    a12 = relative_angle(x1,y1,x2,y2)
    a13 = relative_angle(x1,y1,x3,y3)
    ans1 = abs(a12-a13)*v
    ans2 = (2*pi-abs(a12-a13))*v
    ans = min(ans1,ans2)
    return ans,a12,a13

# 输入123三个士兵的位置，计算1的居中视角
from utils.math1 import relative_angle
def ang_calculation(x1,y1,x2,y2,x3,y3):
    a12 = relative_angle(x1,y1,x2,y2)
    a13 = relative_angle(x1,y1,x3,y3)
    ans1 = abs(a12-a13)
    ans2 = (2*pi-abs(a12-a13))
    if ans1 < ans2:
        ans = (a12 + a13)/2
    else :
        ans = ((a12 + a13)/2 + pi) % (2*pi)
    return ans

# 逐个判断类列表中每一个士兵实例有没有挡路
from utils.math1 import Occlusion_judgment     #def Occlusion_judgment(name1,x1,y1,name2,R2,x2,y2,name3,R3,x3,y3):  判定1的看2的视野是否被3遮挡
def all_Occlusion_judgment(s1,s2,s_lis):
    ans = True
    oc_list = []
    for s3 in s_lis:
        if not s3 == s1 and not s3 == s2:  #排除观察者和被观察者哈
            Oj = Occlusion_judgment(s1.name,s1.x,s1.y,s2.name,s2.radius,s2.x,s2.y,s3.name,s3.radius,s3.x,s3.y)
            if not Oj:
                ans = False
                oc_list.append(s3.name)
    # 输出
    if len(oc_list) == 0:
        print(f'士兵{s1.name}观察士兵{s2.name}的视野没有被遮挡')
        return ans
    else:
        S = ','.join(oc_list)
        print(f'士兵{s1.name}观察士兵{s2.name}的视野被{S}遮挡了哦！！！！！')
        return ans

# 判断是否在视野范围之内
from utils.math1 import Distance_judgment    # def Distance_judgment(name1,vision1,x1,y1,name2,x2,y2):  #判定1的看2有没有超过1的视距
def all_Distance_judgment(s1,s2):
    return Distance_judgment(s1.name,s1.vision,s1.x,s1.y,s2.name,s2.x,s2.y)

# 判断这个士兵是否被其他士兵穿模
from utils.math1 import distance
def all_overlap_judgement(s,s_lis,RR):
    ans = True
    ol_list = []
    for s3 in s_lis:
        if not s3 == s and distance(s.x,s.y,s3.x,s3.y) <= RR:  #排除本体
            ans = False
            ol_list.append(s3.name)
    if len(ol_list) == 0:
        print(f'士兵{s.name}没穿模')
        return ans
    else:
        S = ','.join(ol_list)
        print(f'士兵{s.name}被{S}穿模了哦！！！！')
        return ans


# 输入士兵t时刻视角，视野张角，目标1或目标2对于士兵的相对角，返回是否看到了目标1或2
def update_receive(r_ang,t_ang,v_ang):
    if ((t_ang - v_ang/2) <= r_ang < (t_ang + v_ang/2)) or ((t_ang - v_ang/2) <= r_ang-2*pi < (t_ang + v_ang/2)) :
        return True
    else:
        return False

# 输入士兵是否记忆，是否看到，目标士兵是举旗，返回一个【记忆内容，是否记忆】的列表
def update_remenber(isf,if_rem,if_rec,if_rai,flag):
    if not if_rem and if_rec and if_rai:
        return [flag,True]
    else:
        return isf
    
# 输入系统帧时长，士兵转向速度，t时刻视角，t时刻转头方向，是否看到了目标1或2，是否记忆了目标1或2，返回下一帧的视角
def update_ang(frame,v,t_ang,t_direc,if_rec1,if_rec2,if_rem1,if_rem2):
    if if_rem1 and if_rem2:
        return (t_ang,0)
    elif not if_rem1 and not if_rem2:
        if not if_rec1 and not if_rec2:
            ans = (t_ang+frame*v*t_direc)%(2*pi)
            return (ans,t_direc)
        elif if_rec2 and if_rec1:
            return (t_ang,0)
        else:
            t_direc1 = -t_direc
            ans = (t_ang+frame*v*t_direc1)%(2*pi)
            return (ans,t_direc1)
    else:
        if not if_rec1 and not if_rec2:
            ans = (t_ang+frame*v*t_direc)%(2*pi)
            return (ans,t_direc)
        elif if_rec2 and if_rec1:
            return (t_ang,0)
        else:
            if (if_rem1 and if_rec1) or (if_rem2 and if_rec2):
                t_direc1 = -t_direc
                ans = (t_ang+frame*v*t_direc1)%(2*pi)
                return (ans,t_direc1)
            else :
                return (t_ang,0)

# 输入一个士兵实例，返回其所处在的层级[好久违写个递归]
def update_lev(s,ans):
    if s.target1 != None and s.target2 != None:
        s1 = s.target1
        s2 = s.target2
        return max(update_lev(s1,ans+1),update_lev(s2,ans+1))
    elif s.target1 != None and s.target2 == None:
        s1 = s.target1
        return update_lev(s1,ans+1)
    elif s.target2 != None and s.target1 == None:
        s2 = s.target2
        return update_lev(s2,ans+1)
    else :
        return ans


