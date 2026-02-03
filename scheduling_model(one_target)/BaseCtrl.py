# BaseCtrl.py
import time

def read_sensor_data(ser, return_data=True, timeout=1):
    """
    从串口读取一行数据

    参数:
        ser: 已打开的 serial.Serial
        return_data: 是否返回数据
        timeout: 最大等待时间（秒）

    返回:
        str 或 None
    """
    start_time = time.time()
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8', errors='ignore').strip()
            if data:
                if return_data:
                    return data
                else:
                    return None   # 读到就退出
        if time.time() - start_time > timeout:
            return None
        time.sleep(0.05)

def send_command(ser, command, read_return=False,read_mode=2, timeout_error=3, timeout_receive_finish=0.2):
    """
    使用已打开的串口 ser 发送命令并可选读取返回。

    参数:
        ser: serial.Serial 对象（已打开）
        command: 发送的字符串命令
        read_return: 是否读取返回
        read_mode: 1=END标志结束，2=超时无数据结束
        timeout_error: 最大读取时间
        timeout_receive_finish: 数据间隔超时（模式2）

    返回:
        list[str] 或 None
    """
    responses = []

    for ch in command:
            ser.write(ch.encode('utf-8'))
            time.sleep(0.005)  # 每个字符之间的延时
    print(f"Sent command: {command}")

    if not read_return:
        return None

    start_time = time.time()
    last_time = time.time()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Received: {line}")
                responses.append(line)
                last_time = time.time()
                #模式1：标识符数据结束
                if read_mode == 1 and line == 'END':
                    break
        # 模式2：超时无数据结束
        if read_mode == 2 and time.time() - last_time > timeout_receive_finish:
            break
        # 最大读取时间判断
        if time.time() - start_time > timeout_error:
            print("Read timeout")
            break
        time.sleep(0.01)
    return responses

def reset_input_buffer(ser):
    ser.reset_input_buffer()