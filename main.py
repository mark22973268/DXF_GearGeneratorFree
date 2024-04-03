#main.py
import ezdxf
import numpy as np
import matplotlib.pyplot as plt
#可設定參數


while(1):
    try:
        m=float(input('請輸入模數(單位:mm)Please enter gear module(unit:mm):'))#模數
        break
    except:
        print('你輸入的是非數字，請重新輸入.Not int ,please again')
while(1):
    try:
        tn=int(input('請輸入齒數(整數)Please enter the number of gear teeth:'))#齒數
        break
    except:
        print('你輸入的是非整數，請重新輸入Not int ,please again')
while(1):
    try :
        alpha = float(input('請輸入壓力角(角度)(只能輸入:14.5,20,25)Please enter the pressure angle (angle) (14.5, 20, 25 only):'))#壓力角
        if alpha==14.5 or alpha==20 or alpha==25 :break
        else:print("只能輸入14.5,20,25這3種壓力角 14.5, 20, 25 only")
    except :
        print("只能輸入14.5,20,25這3種壓力角 14.5, 20, 25 only")

while(1):
    try :
        d=float(input('請輸入軸徑 Please enter shaft diameter:'))#軸直徑
        break
    except :
        print('你輸入的是非整數，請重新輸入Not int ,please again')
###
Dp=tn*m#節圓
rp=Dp/2
Db=Dp*np.cos(alpha*np.pi/180)#基圓
rb=Db/2
Da=Dp+2*m#齒頂圓直徑
ra=Da/2
Df=Dp-2.5*m#齒底圓直徑
rf=Df/2
#畫基圓
theta = np.linspace(0, 2 * np.pi, 100)
DbX = rb * np.cos(theta)
DbY = rb * np.sin(theta)
#畫節圓
DpX = rp * np.cos(theta)
DpY = rp * np.sin(theta)
#畫齒頂圓
DaX = ra * np.cos(theta)
DaY = ra * np.sin(theta)
#畫軸
dx = d/2 * np.cos(theta)
dy = d/2 * np.sin(theta)
x=[]
y=[]

#畫齒根
x.append(rf)
y.append(0)
xyPoints=[(rf,0)]


#畫漸開線
final_a=np.degrees(np.arccos(rb/ra))
final_t=ra*np.sin(final_a/180*np.pi)/rb*180/np.pi
# print('final_a=',final_a)
# print('final_t=',final_t)
jump=True
t=0
while(jump):
    if t>=final_t:
        t=final_t
        jump=False
    cbArc=rb*t*np.pi/180#弧長
    a=np.degrees(np.arctan(cbArc/rb))
    inva=(t-a)*np.pi/180#漸開線函數
    xc=(rb/np.cos(a*np.pi/180)) * np.cos(inva)#漸開線公式
    yc=(rb/np.cos(a*np.pi/180)) * np.sin(inva)#漸開線公式
    x.append(xc)
    y.append(yc)
    xyPoints.append((xc,yc))
    t+=1#t為漸開線畫線的精度，+1代表每一度畫一點，變化量越小越準
#鏡射
M=np.array([[1,0],
           [0,-1]],)
mirCx=[]
mirCy=[]
for i in range(len(x)):
    xm,ym,=M.dot([x[i],y[i]])
    mirCx.append(xm)
    mirCy.append(ym)
#旋轉
rpa=np.degrees(np.arccos(rb/rp))
rpt=rp*np.sin(rpa/180*np.pi)/rb#齒型和節圓交接的點，和圓心的夾角
# print('rpa=',rpa)
# print('rpt=',rpt)
theta=(rpt-rpa/180*np.pi)*2 + np.pi/tn
Mr=np.array([[np.cos(theta),-np.sin(theta)],
           [np.sin(theta),np.cos(theta)]],)
xyPointsMir=[]##
for i in range(len(mirCx)):
    ii=len(mirCx)-i-1#倒者走
    xm,ym,=Mr.dot([mirCx[ii],mirCy[ii]])
    x.append(xm)
    y.append(ym)
    xyPointsMir.append((xm,ym))
#將齒根旋轉複製
xgear=[]
ygear=[]
for i in range(1,tn+1):
    theta=np.pi/tn*i*2
    Mr=np.array([[np.cos(theta),-np.sin(theta)],
           [np.sin(theta),np.cos(theta)]],)
    for i in range(len(x)):
        xm,ym,=Mr.dot([x[i],y[i]])
        xgear.append(xm)
        ygear.append(ym)
xgear.append(xgear[0])
ygear.append(ygear[0])

print("請確認預覽圖，確認完請按X. Please confirm the preview image and press X after confirmation.")
plt.plot(dx,dy,DbX,DbY,'-.',DpX,DpY,'-.',DaX,DaY,'-.',xgear,ygear)
plt.axis('equal')
plt.title('Gear')
plt.show()

import math
def c2point(start_point,end_point,center=(0,0)):
    start_angle = math.degrees(math.atan2(start_point[1] - center[1], start_point[0] - center[0]))
    end_angle = math.degrees(math.atan2(end_point[1] - center[1], end_point[0] - center[0]))
    return start_angle,end_angle
#ezdxf
doc = ezdxf.new('R2010')
# 创建模型空间
msp = doc.modelspace()
#畫軸
msp.add_circle(center=(0, 0), radius=d/2)  # 在模型空間中添加一個半徑為5的圓形
#畫齒
for i in range(1,tn+1):
    theta=np.pi/tn*i*2
    Mr=np.array([[np.cos(theta),-np.sin(theta)],
           [np.sin(theta),np.cos(theta)]],)
    xygear=[]
    xygearMir=[]
    for i in range(len(xyPoints)):
        xygear.append(Mr.dot(xyPoints[i]))
    for i in range(len(xyPointsMir)):
        xygearMir.append(Mr.dot(xyPointsMir[i]))
    msp.add_line(xygear[0],xygear[1])
    msp.add_spline(xygear[1:])
    start_angle,end_angle=c2point(xygear[-1],xygearMir[0])#
    msp.add_arc((0,0),ra,start_angle,end_angle)#連結齒頂
    msp.add_spline(xygearMir[:-2])
    msp.add_line(xygearMir[-2],xygearMir[-1])

    theta=np.pi/tn*2
    Mr=np.array([[np.cos(theta),-np.sin(theta)],
           [np.sin(theta),np.cos(theta)]],)
    start_angle,end_angle=c2point(xygearMir[-1],Mr.dot(xygear[0]))#
    msp.add_arc((0,0),rf,start_angle,end_angle)#連結齒底
#
# 保存DXF文件
try:
    fileName=input('請輸入存檔名稱:Please enter the name of file:')
    doc.saveas(fileName+'.dxf')
    print('齒輪生成成功，檔案名稱為:'+fileName+'.dxf' )
    print('Success,name of file is:'+fileName+'.dxf' )
except:
    print('齒輪生成失敗')
    print('Fail')
exit(0)
