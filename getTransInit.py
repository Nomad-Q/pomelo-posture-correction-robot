#This part is mainly finished by Qiu Zeyu and Jin Dongyang.
import math
import numpy as np
from pyntcloud import PyntCloud
import PCA

camera_center_X = -0.1146
camera_center_Y = 0.5678
camera_center_Z = 0.5855

#弧度转成度
def angle_trans(angle):
    angle_x = angle[0] / math.pi * 180
    angle_y = angle[1] / math.pi * 180
    angle_z = angle[2] / math.pi * 180
    print('angle is: (' + str(angle_x) + ', ' + str(angle_y) + ', ' + str(angle_z) + ')')
    # return angle_x, angle_y, angle_z


def xyz_trans(data):
    x = camera_center_X - data[0]/1000
    y = camera_center_Y + data[2]/1000
    z = camera_center_Z - data[1]/1000
    return x, y, z

def getTransInit_final():
    path2 = 'models/kinect_tmp/test2.ply'
    point_cloud_pynt2 = PyntCloud.from_file(path2)
    points2 = point_cloud_pynt2.points
    w2, rows2, center2 = PCA.PCA(points2)
    #-----------------------------
    def distance(x,y,z, data_mean):
        return math.sqrt(pow((x - data_mean[0]), 2)+pow((y - data_mean[2]),2)+pow((z - data_mean[1]),2))

    def findDirection(path, target):
        point_cloud_pynt1 = PyntCloud.from_file(path)
        print(path)
        print(target)
        points = point_cloud_pynt1.points
        data_mean = np.mean(points, axis=0)
        # print(data_mean)
        count = 0
        f = open(path, 'r')
        f_w = open(target, 'w')
        data = f.readlines()
        for i in data[0:]:
            f_w.writelines(i)
            if i == "end_header\n":
                break

        max = 0
        max_x = 0
        max_y = 0
        for i in data[11:]:
            tmp = i.split(" ")
            x = eval(tmp[0])
            z = eval(tmp[1])
            y = eval(tmp[2])

            if distance(x,y,z, data_mean) > max:
                ##垂直不能用这样切割1！！！
                max = distance(x,y,z, data_mean)
                max_x = x
                max_y = y
                print(x, y)
                print("distance:" + str(distance(x,y,z, data_mean)))


            f_w.writelines(i)
            count += 1

        f.close()
        f_w.close()

        f_tr = open(target, 'r')
        data = f_tr.readlines()
        for i in data[0:]:
            if i.__contains__("element vertex"):
                num = i.split(" ")
                f_tr.close()
                break

        file_data = ""
        with open(target, "r") as f:
            for line in f:
                line = line.replace(num[2],str(count)+"\n")
                file_data += line
        with open(target,"w") as f:
            f.write(file_data)
        # row = [[(max_x - data_mean[0])/max, (max_y - data_mean[2])/max, 0], [0, 0, 1], [-(max_y - data_mean[2])/max, (max_x - data_mean[0])/max, 0]]
        print("###################3")
        print(max_x, max_y)
        print(data_mean)

        row = [[(max_x - data_mean[0])/max, 0, (max_y - data_mean[2])/max],
               [0, -1, 0],
               [-(max_y - data_mean[2])/max, 0, (max_x - data_mean[0])/max]]
        answer = [(max_x - data_mean[0])/max, (max_y - data_mean[2])/max]
        return row, answer
    temp = 'models/kinect_tmp'
    path333 = temp + '/test2_1.ply'
    path444 =   temp + '/test3.ply'
    rows2, answer = findDirection(path333, path444)


    print(222)
    x=np.array(answer)
    y=np.array([0,1])
    print('answer is: ')
    print(answer)
    # 两个向量
    Lx=np.sqrt(x.dot(x))
    Ly=np.sqrt(y.dot(y))
    #相当于勾股定理，求得斜线的长度
    cos_angle=x.dot(y)/(Lx*Ly)
    #求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度，初中知识。。
    print(cos_angle)
    angle=np.arccos(answer[1])
    angle_final=angle*360/2/np.pi
    print('angle is:-----------------')
    print(angle_final)
    #变为角度
    if answer[0] > 0:
        angle_final = -50 + angle_final
    else:
        angle_final = -50 - angle_final

    print('Final angle is: '+ str( angle_final))

    x0, y0, z0= xyz_trans(center2)
    print("position is: (" + str(x0) + ', ' + str(y0) + ', ' + str(z0) + ')')

    return x0, y0, z0, angle_final
    #----------------------------------------------------------------



