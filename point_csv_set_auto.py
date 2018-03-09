from argparse import ArgumentParser
import pandas as pd
import sys
import os.path
import numpy as np
import binascii
import socket
import re
import time 

#SOURCE_ADDR = 'localhost'
SOURCE_ADDR = '192.168.1.10'
SOURCE_PORT = 10050 

#DESTINATION_ADDR = 'localhost'
DESTINATION_ADDR = '192.168.1.99'
DESTINATION_PORT = 10040 

def set_data_to_yac(dir_name, file_name):
    ### LOAD CSV FILE START ###
    file_path = os.path.join(dir_name, file_name)
    print('check ', file_path)

    if 'csv' not in file_name:
        print("->file is not csv")
        return False

    if not os.path.exists(file_path):
        print("->file not exist")
        return False

    print('loading...')
    df = pd.read_csv(file_path, header=None)
    ### LOAD CSV FILE END ###

    ### SET B001 START ###
    df_len = len(df.index)
    print('Number of data: ', df_len)

    print('Writing the number of data to B001')
    # header
    yerc = "<59><45><52><43>"   # fixed
    header_size = "<20><00>"    # fixed
    data_size = "<01><00>"      # dynamic (fixed: 1 byte for byte type write)
    reserved1 = "<03><01><00><00>"   # fixed
    blocked = "<00><00><00><00>"    # fixed
    reserved2 = "<39><39><39><39><39><39><39><39>"  # fixed
    header = yerc + header_size + data_size + reserved1 + blocked + reserved2

    # sub header
    command = "<7A><00>"    # byte type
    data_index = "<01><00>"    # B001
    request_num = "<01>"    # fixed
    compute = "<02>"    # read: Set_Attribute_All ：0x02
    sub_header = command + data_index + request_num + compute

    # data
    data = "<" + '{:02X}'.format(df_len) + ">"   # no data for read

    # request
    ascii_str = header + sub_header + data

    # ascii code to binary
    data = bytearray()
    matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
    for match in matches:
        data += bytearray.fromhex(match)

    # send data
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.bind((SOURCE_ADDR, SOURCE_PORT))
    client.sendto(data, (DESTINATION_ADDR, DESTINATION_PORT))
    print('sent>> ', binascii.hexlify(data))

    # answer
    # header 20 byte
    # sub header 8 byte
    # data 1 byte
    recv_data, addr = client.recvfrom(4096)
    # TODO check last 1 byte (= B002)
    print('recv<< ', binascii.hexlify(recv_data))
    print('done')
    ### SET B001 END ###

    ### SET P START ###
    # 1 loop is 1 line
    print('Writing position data...')
    for i, v in df.iterrows():
        write (to_ascii(i, 4),
               to_ascii(v[0], 4), to_ascii(v[1], 4), 
               to_ascii(v[2], 4), to_ascii(v[3], 4),
               to_ascii(v[4], 4), to_ascii(v[5], 4))
    print('done')
    ### SET P END ###

    return True

def to_ascii(dec, n_byte):
    hex_str = to_hex_le(dec, n_byte)
    li = [(i+j) for (i,j) in zip(hex_str[::2], hex_str[1::2])]
    ascii_code = '<' + '><'.join(li) + '>'
    return ascii_code

'''
to hex little endian with two's complement
'''
def to_hex_le(dec, n_byte):
    # numpy int to premitive int
    dec = np.asscalar(dec)

    if n_byte is 2:
        return dec.to_bytes(2, 'little', signed=True).hex().upper()
    elif n_byte is 4:
        return dec.to_bytes(4, 'little', signed=True).hex().upper()
    elif n_byte is 8:
        return dec.to_bytes(8, 'little', signed=True).hex().upper()
    else:
        return 'error'

'''
write position data to P[i]
'''
def write(i, x, y, z, r_x, r_y, r_z):
    #print(i, x, y, z, r_x, r_y, r_z)

    # header
    yerc = "<59><45><52><43>"   # fixed
    header_size = "<20><00>"    # fixed
    data_size = "<34><00>"      # dynamic (fixed: 52 byte for position)
    reserved1 = "<03><01><00><00>"   # fixed
    blocked = "<00><00><00><00>"    # fixed
    reserved2 = "<39><39><39><39><39><39><39><39>"  # fixed
    header = yerc + header_size + data_size + reserved1 + blocked + reserved2

    # sub header
    command = "<7F><00>"    # dynamic
    data_index = i    # dynamic: max: 99
    request_num = "<11>"    # dynamic (fixed: robot coordinate value 17)
    compute = "<02>"    # dynamic: Set_Attribute_All ：0x02
    sub_header = command + data_index + request_num + compute

    # data
    data_type = "<00><00><00><00>"  # fixed
    form = "<00><00><00><00>"  # fixed
    tool_num = "<00><00><00><00>"  # fixed
    user_coor_num = "<00><00><00><00>"  # fixed
    custom_form = "<00><00><00><00>"  # fixed
    data_common_part = data_type + form + tool_num + user_coor_num + custom_form
    coor1 = x  # dynamic
    coor2 = y  # dynamic
    coor3 = z  # dynamic
    coor4 = r_x  # dynamic
    coor5 = r_y  # dynamic
    coor6 = r_z  # dynamic
    coor7 = "<00><00><00><00>"  # fixed
    coor8 = "<00><00><00><00>"  # fixed
    coors = coor1 + coor2 + coor3 + coor4 + coor5 + coor6 + coor7 + coor8
    data = data_common_part + coors

    # request
    ascii_str = header + sub_header + data

    # ascii code to binary
    data = bytearray()
    matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
    for match in matches:
        data += bytearray.fromhex(match)

    # send data
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.bind((SOURCE_ADDR, SOURCE_PORT))
    client.sendto(data, (DESTINATION_ADDR, DESTINATION_PORT))
    print('sent>> ', binascii.hexlify(data))

    # answer
    recv_data, addr = client.recvfrom(4096)
    print('recv<< ', binascii.hexlify(recv_data))



'''
for csv load
'''
def parser():
    usage = 'Usage: python {} [-d DIRECTORY] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('-d', '--directory',
                           dest='dir_name',
                           help='directory name')
    args = argparser.parse_args()
    return args.dir_name

    
if __name__ == '__main__':
    DEFAULT_DIR = 'csv_files'
    dir_name = parser()
    print('directory name: ', dir_name)

    if dir_name is None:
        print('set default dir name', DEFAULT_DIR)
        dir_name = DEFAULT_DIR

    if not os.path.exists(dir_name):
        print('directory "', dir_name, '"not exist')
        sys.exit()

    files = os.listdir(dir_name)
    print(files)

    # check all files in the directory
    for file_name in files:
        success = set_data_to_yac(dir_name, file_name)
        if not success:
            continue

        ### START JOB START ###
        print('start')

        # header
        yerc = "<59><45><52><43>"   # fixed
        header_size = "<20><00>"    # fixed
        data_size = "<04><00>"      # dynamic (fixed: 4 byte for job start)
        reserved1 = "<03><01><00><00>"   # fixed
        blocked = "<00><00><00><00>"    # fixed
        reserved2 = "<39><39><39><39><39><39><39><39>"  # fixed
        header = yerc + header_size + data_size + reserved1 + blocked + reserved2

        # sub header
        command = "<86><00>"
        data_index = "<01><00>"    # dynamic: fixed
        request_num = "<01>"    # fixed
        compute = "<10>"    # Set_Attribute_Single ：0x10
        sub_header = command + data_index + request_num + compute

        # data
        job_start = "<01><00><00><00>"    # fixed
        data = job_start

        # request
        ascii_str = header + sub_header + data

        # ascii code to binary
        data = bytearray()
        matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
        for match in matches:
            data += bytearray.fromhex(match)

        # send data
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        client.bind((SOURCE_ADDR, SOURCE_PORT))
        client.sendto(data, (DESTINATION_ADDR, DESTINATION_PORT))
        print('sent>> ', binascii.hexlify(data));

        # answer
        recv_data, addr = client.recvfrom(4096)
        print('recv<< ', binascii.hexlify(recv_data))

        print('done')
        ### START JOB END ###

        ### WAIT JOB COMPLETE START ###
        while True:
            print("wait for job completion")
            for wait_time in range(10): # Delay for 10s
                print('.', end='', flush=True)
                time.sleep(1)
            print()

            print("check job status")
            # header
            yerc = "<59><45><52><43>"   # fixed
            header_size = "<20><00>"    # fixed
            data_size = "<00><00>"      # dynamic (fixed: 0 byte for byte type read)
            reserved1 = "<03><01><00><00>"   # fixed
            blocked = "<00><00><00><00>"    # fixed
            reserved2 = "<39><39><39><39><39><39><39><39>"  # fixed
            header = yerc + header_size + data_size + reserved1 + blocked + reserved2

            # sub header
            command = "<7A><00>"    # byte type
            data_index = "<02><00>"    # B002
            request_num = "<01>"    # fixed
            compute = "<01>"    # read: Get_Attribute_All ：0x01
            sub_header = command + data_index + request_num + compute

            # data
            data = ""   # no data for read

            # request
            ascii_str = header + sub_header + data

            # ascii code to binary
            data = bytearray()
            matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
            for match in matches:
                data += bytearray.fromhex(match)

            # send data
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            client.bind((SOURCE_ADDR, SOURCE_PORT))
            client.sendto(data, (DESTINATION_ADDR, DESTINATION_PORT))
            print('sent>> ', binascii.hexlify(data))

            # answer
            # header 20 byte
            # sub header 8 byte
            # data 1 byte
            recv_data, addr = client.recvfrom(4096)
            # TODO check last 1 byte (= B002)
            print('recv<< ', binascii.hexlify(recv_data))
            result_flag = recv_data[-1]

            if result_flag:
                print('complete!')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print()
                time.sleep(1)
                break
        ### WAIT JOB COMPLETE END ###



