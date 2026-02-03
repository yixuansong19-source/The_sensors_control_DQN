import BaseCtrl
import lora
import fake_device
import serial
import random
import Envir as Env

send_port='COM15'
receive_port='COM14'
baudrate=9600

def predict(s,MOCK=True):
    if MOCK :
        predict_action=random.randint(0,1)
    else:
        
    return predict_action

def open_lora():
    ser_send=serial.Serial(send_port,baudrate,timeout=0.1)
    ser_receive=serial.Serial(receive_port,baudrate,timeout=0.1)
    return ser_send,ser_receive

def main():
    ser_send,ser_receive=open_lora()

    BaseCtrl.reset_input_buffer(ser_send)
    BaseCtrl.reset_input_buffer(ser_receive)

    s=[{0,0,0,0}]   #s[0-2]:target_localtion   s[3]:pre_sensor


    try:
        while(True):
            s=lora.receive_data_pc(ser_receive,0)
    finally:
        ser_send.close()
        ser_receive.close()