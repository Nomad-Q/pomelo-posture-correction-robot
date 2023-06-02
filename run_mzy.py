#This part is mainly finished by Ma Zhuoyuan.
import os
import PointCloud
import reload_mzy as reload

#将temp改成你需要存放柚子点云的相对路径
temp = 'models/kinect_tmp'
#path1中储存点云的初始信息，也即摄像机拍摄到的画面信息
path1 =   temp + '/test.ply'
#path2中存储经过RGB信息和位置信息筛选过的属于柚子的信息
path2 =   temp + '/test1.ply'
#path3中存储去掉颜色信息的纯净的柚子点云信息
path3 =   temp + '/test2.ply'
#path3_1中存储二维化之后的柚子点云信息
path3_1 = temp + '/test2_1.ply'
def shoot():
    if os.path.exists(path1):
        os.remove(path1)
    pcl = PointCloud.Cloud(file=path1, depth=True)
    pcl = PointCloud.Cloud(file=path1, color=True)

def reload_total():
    # 筛选点云颜色，高度
    reload.load_ply(path1, path2)
    reload.remove_color(path2, path3)
    reload.remove_unreliable_point(path3, path3_1)
