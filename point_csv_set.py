from argparse import ArgumentParser
import pandas as pd
import sys
import os.path
import numpy as np
import binascii
import socket
import re

def set_data_to_yac(dir_name, file_name):
    if 'csv' not in file_name:
        print("file is not csv")
        return

    file_path = os.path.join(dir_name, file_name)
    if not os.path.exists(file_path):
        print("file not exist")
        return

    print('load ', file_path)
    df = pd.read_csv(file_path, header=None)
    df_len = len(df.index)

    # 1 loop is 1 line
    for i, v in df.iterrows():
        write (to_ascii(i, 4),
               to_ascii(v[0], 4), to_ascii(v[1], 4), 
               to_ascii(v[2], 4), to_ascii(v[3], 4),
               to_ascii(v[4], 4), to_ascii(v[5], 4))

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

def write(i, x, y, z, r_x, r_y, r_z):
    #print(i, x, y, z, r_x, r_y, r_z)
    #SOURCE_ADDR = 'localhost'
    SOURCE_ADDR = '192.168.1.10'
    SOURCE_PORT = 10050 

    #DESTINATION_ADDR = 'localhost'
    DESTINATION_ADDR = '192.168.1.99'
    DESTINATION_PORT = 10040 

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
    padding = "<00><00>"
    sub_header = command + data_index + request_num + compute + padding

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

    for file_name in files:
        set_data_to_yac(dir_name, file_name)

        # TODO: jobstart
        # TODO: wait

