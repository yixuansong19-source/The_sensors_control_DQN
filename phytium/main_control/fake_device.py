# fake_device.py
import time
import queue
import threading


class FakeSerial:
    def __init__(self, name="FAKE", timeout=0.1):
        self.name = name
        self.timeout = timeout
        self.rx = queue.Queue()
        self.tx = queue.Queue()
        self.is_open = True

    @property
    def in_waiting(self):
        return self.rx.qsize()
    
    def reset_input_buffer(self):
        while not self.rx.empty():
            self.rx.get()

    def write(self, data: bytes):
        msg = data.decode(errors='ignore').strip()
        print(f"[fake {self.name} WRITE] {msg}")
        self.tx.put(msg)

    def readline(self):
        try:
            line = self.rx.get(timeout=self.timeout)
            return (line + "\n").encode()
        except queue.Empty:
            return b""

    def close(self):
        self.is_open = False
        print(f"[{self.name}] closed")

    def inject(self, line: str):
        self.rx.put(line)


# ================= 模拟 LoRa =================

def run_fake_lora(ser):
    def worker():
        power = 1
        while ser.is_open:
            ser.inject(f"1,{power}")   # 模拟 power 命令
            ser.inject(f"END")
            power = 1 - power
            time.sleep(2)

            while not ser.tx.empty():
                cmd = ser.tx.get()
                print(f"[FAKE LORA RECEIVED] {cmd}")

    threading.Thread(target=worker, daemon=True).start()


# ================= 模拟 传感器 =================

def run_fake_sensor(ser):
    def worker():
        while ser.is_open:
            while not ser.tx.empty():
                cmd = ser.tx.get()
                print(f"[FAKE SENSOR RECEIVED] {cmd}")
                if cmd == '1':
                    ser.inject("60,35")
                    ser.inject("END")
            time.sleep(0.05)

    threading.Thread(target=worker, daemon=True).start()
