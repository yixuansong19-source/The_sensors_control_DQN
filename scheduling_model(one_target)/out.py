import math
import serial
import time
import re
import os
import random
import numpy as np
import csv
from parl.env import CompatWrapper
from cartpole_model import CartpoleModel
from cartpole_agent import CartpoleAgent
from parl.algorithms import DQN  # 导入 DQN 算法
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 加载环境
from Envir import Env
import BaseCtrl
import lora
import fake_device


send_port='COM15'
receive_port='COM14'
baudrate=9600

log_file = open("tracking_log.csv", mode='w', newline='')
logger = csv.writer(log_file)
logger.writerow(["timestamp", "x", "y", "z", "speed", "direction_xy", "direction_z", "action"])

sensors = [[10, 20, 0], [90,70,0], [130, 155, 0]]
pre_sensor = 1

# 顶部添加
_agent_cache = None

class Visualizer:
    def __init__(self, sensors):
        self.sensors = sensors
        self.trajectory = []  # 保存轨迹点
        self.current_sensor = None
        self.fig, self.ax = plt.subplots()
        self.target_dot, = self.ax.plot([], [], 'ro', label="Target")
        self.trajectory_line, = self.ax.plot([], [], 'r--', alpha=0.5, label="Trajectory")
        self.sensor_dots = []
        self.active_sensor_dot = None
        self.init_plot()

    def init_plot(self):
        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 200)
        self.ax.set_title("Target Tracking")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        for s in self.sensors:
            dot, = self.ax.plot(s[0], s[1], 'bo', label="Sensor", markersize=6)
            self.sensor_dots.append(dot)
        self.ax.legend()

    def update(self, location, active_sensor):
        self.trajectory.append(location[:2])  # 只取 x, y 坐标
        xs, ys = zip(*self.trajectory)  # 提取轨迹的 x 和 y 坐标
        self.trajectory_line.set_data(xs, ys)  # 更新轨迹线
        self.target_dot.set_data(location[0], location[1])  # 更新目标位置

        # 更新高亮传感器
        if self.active_sensor_dot:
            self.active_sensor_dot.remove()
        sensor_pos = self.sensors[active_sensor]
        self.active_sensor_dot, = self.ax.plot(sensor_pos[0], sensor_pos[1], 'go', markersize=12, label="Active Sensor")

        plt.pause(0.01)  # 实时刷新


    def show(self):
        plt.show()

def load_model_once():
    global _agent_cache
    if _agent_cache is not None:
        return _agent_cache

    # 创建模型
    obs_dim = 4
    act_dim = 3
    model = CartpoleModel(obs_dim=obs_dim, act_dim=act_dim)

    # 设置 DQN 参数
    gamma = 0.99
    lr = 1e-3
    algorithm = DQN(model, gamma=gamma, lr=lr)

    # 创建 agent 并加载模型
    agent = CartpoleAgent(algorithm=algorithm, act_dim=act_dim)
    agent.load_model('./inference_model')

    _agent_cache = agent
    return agent

def predict(latest_location, speed, direction):
    # 创建环境
    env = Env(target_start_position=latest_location, target_direction=direction, target_speed=speed)

    # 获取初始状态
    obs = env.get_initial_obs()

    # 使用已加载的 agent
    agent = load_model_once()

    # 推理得到动作
    action = agent.sample(obs)
    return action

def receive_from_serial(ser, use_mock=False):
    global pre_sensor
    try:
        if use_mock:
            time.sleep(0.2)
            # 模拟串口数据，每次调用逐行返回
            test_angle = random.randint(0, 180)
            test_distance = random.randint(0, 40)
            test_sender = pre_sensor

            test_lines = [
                "OnRxDone",
                "Recv:",
                f"{test_angle},{test_distance}",
                f"{test_sender}",
                "rssi = -120, snr = -8"
            ]

            count = 0
            angle = distance = sender = None

            while count < len(test_lines):
                line = test_lines[count].strip()
                print(f"[SERIAL] Line: {line}")

                if count == 2 and re.match(r'^\d+,\d+$', line):
                    angle, distance = map(int, line.split(','))
                elif count == 3 and re.match(r'^\d+$', line):
                    sender = int(line)
                    print(f"recv: {angle},{distance} from:{sender}")
                    return angle, distance, sender

                count += 1

        else:
            # 实际串口读取逻辑
            angle = distance = sender = None
            count = 0
            start_time=time.time()
            while time.time()-start_time < 3 :
                while count < 2:
                    line = BaseCtrl.read_sensor_data(ser, True)
                    print(f"[SERIAL] Line: {line}")

                    if count == 0 and line and re.match(r'^\d+,\d+,\d+$', line):
                        angle, distance ,sender = map(int, line.split(','))
                        count += 1
                        print(f"recv: {angle},{distance} from:{sender}")
                        return angle, distance, sender
            if time.time()-start_time>=3:
                print('timeout...')
                return None
           
    except serial.SerialException as e:
        print(f"串口错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

def send(action, isON, ser):
    addr_target = 10
    DATA = '11\r\n' if isON else '00\r\n'
    command_list = [DATA, DATA, '+++\r\n']
    lora.send_data(ser, command_list, addr_target)

def main():
    global count
    visualizer = Visualizer(sensors)

    # 初始化串口
    use_mock = False  # 设置为True使用模拟
    if use_mock:
        ser_send = fake_device.FakeSerial("SEND")
        ser_receive = fake_device.FakeSerial("RECEIVE")
        fake_device.run_fake_lora(ser_send)
        fake_device.run_fake_sensor(ser_receive)
    else:
        ser_send = serial.Serial(send_port, baudrate, timeout=1)
        ser_receive = serial.Serial(receive_port, baudrate, timeout=1)

    try:
        #设置初始参数
        global pre_sensor
        initial_location = [ 0 , 0 , 30 ]
        initial_speed = 10
        initial_direction = [ 10 , 0 ]
        initial_action = predict(initial_location ,initial_speed ,initial_direction)+1 
        # initial_action = 1
        send(initial_action , True, ser_send)
        initial_time = time.time()

        pre_location = initial_location
        pre_speed = initial_speed
        pre_direction = initial_direction
        pre_sensor = initial_action-1
        pre_time = initial_time
        latest_location = [ 0 , 0 , 30 ]

        while(True):
            result = receive_from_serial(ser_receive, use_mock)
            if result is None:
                print("接收失败，跳过本轮")
                time.sleep(0.1)
                continue
            angle, distance, sender = result
            AtoB_time = time.time() - pre_time
            direction = [ angle , 0 ]
           
            angle_xy = math.radians(angle)
            angle_z = math.radians(0)

            sin_value = [math.sin(angle_xy), math.sin(angle_z)]
            cos_value = [math.cos(angle_xy), math.cos(angle_z)]
            
            latest_location[0]=latest_location[0]+10
            latest_location[1]=latest_location[1]+10
            latest_location[2]=0

            square_AtoB = 0
            for i in range(0 , 2):
                square_AtoB += math.pow(( latest_location[i] - pre_location[i]) , 2 )
            AtoB_distance=math.sqrt(square_AtoB)
            latest_speed=AtoB_distance / AtoB_time

            latest_direction = [ 0 , 0 ]
            latest_direction[0] = math.degrees(math.atan2((latest_location[0] - pre_location[0]), (latest_location[1] - pre_location[1])))
            z_distance = math.sqrt((latest_location[0] - pre_location[0]) ** 2 +(latest_location[1] - pre_location[1]) ** 2)
            xy_difference = latest_location[2] - pre_location[2]
            latest_direction[1] = math.degrees(math.atan2(xy_difference, z_distance))
            latest_sensor=predict(latest_location ,latest_speed ,latest_direction)%2 + 1
            
            # 用模拟数据替代真实预测
            latest_sensor=random.randint(1,2)

            if pre_sensor == 1 :
                latest_sensor = 2
            elif pre_sensor == 2 :
                latest_sensor = 1
            

            print(f'the next sensor:{latest_sensor}')

            if latest_sensor!=pre_sensor:
                send(latest_sensor , True, ser_send)
            else:
                send(latest_sensor , True, ser_send)
                print('the same sensor')
            pre_sensor=latest_sensor
            pre_time = time.time()
            pre_location = latest_location
            pre_direction = latest_direction
            pre_speed = latest_speed
            logger.writerow([time.time(), latest_location[0], latest_location[1], latest_location[2], latest_speed, latest_direction[0], latest_direction[1], latest_sensor])
            time.sleep(0.05)
            visualizer.update(latest_location, latest_sensor-1)
            plt.pause(0.001)
    finally:
        log_file.close()
        ser_send.close()
        ser_receive.close()

if __name__ == "__main__":
    main()