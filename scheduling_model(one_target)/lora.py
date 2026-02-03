# lora.py
import BaseCtrl
import time
import re

def Setup(ser, addr_local):
    set_addr='AT+CADDRSET='+str(addr_local)+'\r\n'
    BaseCtrl.send_command(ser,set_addr)

def mode_receive(ser):
    setting_receive='AT+CRXS=470500000,5,0,1,1\r\n'
    BaseCtrl.send_command(ser,setting_receive)

def mode_send_setup(ser, addr_target):
    set_target='AT+CTXADDRSET='+str(addr_target)+'\r\n'
    setting_target='AT+CTX=470500000,5,0,1,21,1\r\n'
    BaseCtrl.send_command(ser,set_target,True)
    time.sleep(0.2)
    BaseCtrl.send_command(ser,setting_target,True)

def mode_send_exit(ser):
    time.sleep(0.2)
    words_exit='+++\r\n'
    BaseCtrl.send_command(ser,words_exit,True)

def receive_data_pc(ser, function):
    '''
    function:
        0: read func
        1: target_info[]={angle,distance,pre_sensor}
    '''
    count=0
    func=0
    target_info={0,0,0}
    line_count=[1,1]    #每个功能所要读取的数据段的行数
    time_start=time.time()

    while time.time()-time_start<3:
        line = BaseCtrl.read_sensor_data(ser, True)
        print(f"[SERIAL] Line: {repr(line)}")
        
        if not line:
            continue
        
        line = line.strip()
        
        if count < line_count[function]:
            if function == 1 and count == 0 and re.match(r'^\d+,\d+,\d+,\d+$', line):
                func,target_info[0],target_info[1],target_info[2] = map(int, line.split(','))
                count += 1
        
        elif count == line_count[function]:
            if re.match(r'from'):
                if function == func :
                    if function==1:
                        print(f'angle: {target_info[0]},distance:{target_info[1]},sender:{target_info[2]}\n')
                        BaseCtrl.reset_input_buffer(ser)
                        return target_info
                else:
                    print('Receive does not match the function')
                    BaseCtrl.reset_input_buffer(ser)
                    return None
            else:
                continue
        
        else:
            print('something is wrong...')
            BaseCtrl.reset_input_buffer(ser)
            return None
    if time.time()-time_start>=3:
        print('timeout...')
        return None
    
def receive_data_pie(ser, function):
    '''
    function:
        0: s[]={target_localtion_x,target_localtion_y,target_localtion_z,pre_sensor}
        1: power
    '''
    count=0
    func=0
    power=0
    line_count=[0,1]    #每个功能所要读取的数据段的行数
    time_start=time.time()

    mode_receive(ser)

    while time.time()-time_start<3:
        line = BaseCtrl.read_sensor_data(ser, True)
        print(f"[SERIAL] Line: {repr(line)}")
        
        if not line:
            continue
        
        line = line.strip()
        
        if count < line_count[function]:
            if function == 1 and count == 0 and re.match(r'^\d[01]$', line):
                func = int(line[0])
                power = line[1]
                count += 1
        
        elif count == line_count[function]:
            if line == 'from: 9':
                if function == func:
                    result = (power == '1')
                    print(f'on/off: {"on" if result else "off"}\n')
                    BaseCtrl.reset_input_buffer(ser)
                    return result
                else:
                    print('Receive does not match the function')
                    BaseCtrl.reset_input_buffer(ser)
                    return None
            else:
                continue
        
        else:
            print('something is wrong...')
            BaseCtrl.reset_input_buffer(ser)
            return None
    if time.time()-time_start>=3:
        print('timeout...')
        return None
    
def send_data(ser, command_list, addr_target):
    mode_send_setup(ser, addr_target)
    try:
        for cmd in command_list:
            BaseCtrl.send_command(ser, cmd)
    finally:
        mode_send_exit(ser)
    
