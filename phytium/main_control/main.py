# main.py
import fake_device as FK
import serial
import time
import BaseCtrl
import lora
import re

addr_local=1
addr_target=10
lora_port = "/dev/ttyUSB0"
sensor_port = "/dev/ttyUSB1"
baudrate = 9600

serial_mock=0  #0:无模拟  1:模拟lora  2:模拟sensor  3:模拟lora和sensor

def serial_open():
    if serial_mock == 0:    #sensor真实 lora真实
        ser_lora = serial.Serial(lora_port, 9600, timeout=0.1)
        ser_sensor = serial.Serial(sensor_port, 9600, timeout=0.1)

    elif serial_mock == 1:    #sensor真实 lora模拟
        ser_sensor = serial.Serial(sensor_port, 9600, timeout=0.1)
        ser_lora = FK.FakeSerial("lora")
        FK.run_fake_lora(ser_lora)

    elif serial_mock == 2:  #sensor模拟 lora真实
        ser_lora = serial.Serial(lora_port, 9600, timeout=0.1)
        ser_sensor = FK.FakeSerial("sensor")
        FK.run_fake_sensor(ser_sensor)

    elif serial_mock == 3:  #sensor模拟 lora模拟
        ser_lora = FK.FakeSerial("lora")
        ser_sensor = FK.FakeSerial("sensor")
        FK.run_fake_lora(ser_lora)
        FK.run_fake_sensor(ser_sensor)

    return ser_lora, ser_sensor

def main():
    #打开串口
    ser_lora, ser_sensor = serial_open()
    
    #初始化
    lora.Setup(ser_lora,addr_local)
    BaseCtrl.reset_input_buffer(ser_lora)
    BaseCtrl.reset_input_buffer(ser_sensor)
    try:
        #将数据从lora模块中取出
        while True:
            power=lora.receive_data(ser_lora,1)
            if power:
                data=BaseCtrl.send_command(ser_sensor,'1',True,1)
                if data:
                    angle = distance = None
                    for line in data:
                        if re.match(r'^\d+,\d+$', line):
                            angle, distance = map(int, line.split(','))
                            break
                    if angle is None or distance is None:
                        print("No valid sensor data received")
                        continue
                    print(f'angle:{angle},distance:{distance}')
                    command_list=[]
                    command_list.append(f"{angle},{distance},{addr_local}\r\n")
                    lora.send_data(ser_lora,command_list,addr_target)
            time.sleep(0.05)
    except Exception as e:
        print("Error:", e)
    finally:
        ser_lora.close()
        ser_sensor.close()


if __name__ == "__main__":
    main()