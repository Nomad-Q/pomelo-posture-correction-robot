
import robotcontrol as rc
import Femto.getTransInit as gt
import run_mzy as run
import sys
import serial
import time

def main():
    robot = rc.Auboi5Robot()
    speed = 0.5
    rc.init_robot(robot, speed)
    i = 0
    ser = serial.Serial('COM3', 9600, timeout=1)
    while True:
        print("num: "+ str(i))
        time1 = time.time()
        print("time1: "+str(time1))
        #开始拍摄点云
        run.shoot()
        print("finish shoot")
        time2 = time.time()-time1
        print("time2: "+str(time2))
        #处理点云
        run.reload_total()
        print("finish reload")
        time3 = time.time()-time1
        print("time3: "+str(time3))
        #计算位姿
        x, y, z, angle_final = gt.getTransInit_final()
        print("finish gettransInit")
        time4 = time.time()-time1
        print("time4: "+str(time4))
        #位姿矫正
        rc.move2Target(robot, x, y, z, angle_final, ser)
        print("finish move")
        time5 = time.time()-time1
        print("time5: "+str(time5))
        time_total = time.time() - time1
        print("time_total: " + str(time_total))
        i+=1

    sys.exit()



if __name__ == '__main__':
    main()
