import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("❌ 未检测到任何串口设备")
        return

    print("✅ 检测到以下串口设备：\n")
    for port in ports:
        print(f"设备名     : {port.device}")
        print(f"描述       : {port.description}")
        print(f"硬件ID     : {port.hwid}")
        print("-" * 40)

if __name__ == "__main__":
    list_ports()
