import os
import serial
import keyboard
import time
import threading

# 打开串口
ser = serial.Serial('COM4', 9600, timeout=1)
file_path = 'example.txt'
interval = 0.1  # 检测文件变化的时间间隔，单位为秒


# 定义一个函数，用于从键盘读取按键，并发送数据到串口qzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqzqqzqzqz
def send_data():
    while True:
        if keyboard.is_pressed('q'):
            # 发送字符“o;”
            ser.write(b'o;')
        elif keyboard.is_pressed('z'):
            # 发送字符“c;”
            ser.write(b'c;')
        # 等待一段时间，避免过多占用CPU资源
        time.sleep(0.01)


# 定义一个函数，用于从命令行读取变量A的值，并发送数据到串口qzqzqzqzqzqqzqzqz
def send_variable():
    while True:
        # 读取变量A
        A = input("请输入变量A的值：")
        # 根据A的值发送数据到串口
        if A == 'o':
            ser.write(b'o;')
        elif A == 'c':
            ser.write(b'c;')


# 获取文件的修改时间
def get_modify_time(file_path):
    return os.stat(file_path).st_mtime


# 检测文件是否发生变化
def check_file_change(file_path):
    modify_time = get_modify_time(file_path)
    time.sleep(interval)
    if modify_time != get_modify_time(file_path):
        return True
    return False


# 读取文件内容并打印
def read_file(file_path):
    global oldcontent
    oldcontent = ""
    with open(file_path, 'r') as f:
        content = f.read()
        if oldcontent != content:
            oldcontent = content
            print(oldcontent)
            if oldcontent == 'open':
                ser.write(b'o;')
            elif oldcontent == 'close':
                ser.write(b'c;')


def check_and_print():
    while True:
        if check_file_change(file_path):
            read_file(file_path)


# 创建三个线程，分别用于从键盘读取按键、从命令行读取变量A / 实时读取txt文件（二选一）
t1 = threading.Thread(target=send_data)
##t2 = threading.Thread(target=send_variable)
t3 = threading.Thread(target=check_and_print)

# 启动线程
t1.start()
##t2.start()
t3.start()

# 等待线程结束
t1.join()
# t2.join()
t3.join()
