from argparse import ArgumentParser
import pandas as pd
import sys
import os.path
import numpy as np
import binascii
import socket
import re
import time
import csv

#SOURCE_ADDR = 'localhost'
SOURCE_ADDR = '192.168.1.10'
SOURCE_PORT = 10050

#DESTINATION_ADDR = 'localhost'
DESTINATION_ADDR = '192.168.1.99'
DESTINATION_PORT = 10040

# WIP: まだつかってない
class socket_client:
    def __init__(self, src_addr, src_port, dst_addr, dst_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.client.bind((src_addr, src_port))

        self.dst_addr = dst_addr
        self.dst_port = dst_port


    def send_data(self, data):
        # send data
        self.client.sendto(data, (self.dst_addr, self.dst_port))
        print('sent>> ', binascii.hexlify(data))

        # answer
        recv_data, addr = self.client.recvfrom(4096)
        print('recv<< ', binascii.hexlify(recv_data))
        return recv_data

# WIP: まだつかってない
class udp_packet:
    def __init__(self):
        self.utils = utils()
        self.header = ''
        self.sub_header = ''
        self.data = ''

    def set_header(self, data_size):
        # header
        yerc = "<59><45><52><43>"   # fixed
        header_size = "<20><00>"    # fixed
        #data_size = data_size      # dynamic (fixed: 1 byte for byte type write)
        reserved1 = "<03><01><00><00>"   # fixed
        blocked = "<00><00><00><00>"    # fixed
        reserved2 = "<39><39><39><39><39><39><39><39>"  # fixed
        self.header = yerc + header_size + data_size + reserved1 + blocked + reserved2

    def set_sub_header(self, command, data_index, request_num, compute):
        #command = "<7A><00>"    # byte type
        #data_index = "<01><00>"    # B001
        #request_num = "<01>"    # fixed
        #compute = "<02>"    # read: Set_Attribute_All ：0x02
        padding = "<00><00>"
        self.sub_header = command + data_index + request_num + compute + padding
    
    def set_data(self, data):
        self.data = data

    def clear_data(self):
        self.header = ''
        self.sub_header = ''
        self.data = ''

    def run(self, files):
        print(files)
        # for file_name in files:
        #     point_set_success = set_data_to_yac(dir_name, file_name, client)
        #     if not point_set_success:
        #         continue

        #     start_job(client)

        #     print('took ' + str(time.time() - start))

        #     wait_job_complete(client)



    #set_data_to_yac(self, dir_name, file_name, client):
    # start job
    # wait work complete
    # set b001
    # set_b000_to_0
    # set_data_to_yac
    # write
    # servo on
    # set b000 to 0

# WIP: まだつかってない
class utils:
    def to_ascii(self, dec, n_byte):
        hex_str = to_hex_le(dec, n_byte)
        li = [(i+j) for (i,j) in zip(hex_str[::2], hex_str[1::2])]
        ascii_code = '<' + '><'.join(li) + '>'
        return ascii_code

    def to_hex_le(self, dec, n_byte):
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

    def ascii_to_binary(self, ascii_str):
        # ascii code to binary
        data = bytearray()
        matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
        for match in matches:
            data += bytearray.fromhex(match)
        return data


def send_data(client, data):
    # send data
    client.sendto(data, (DESTINATION_ADDR, DESTINATION_PORT))
    print('sent>> ', binascii.hexlify(data))

    # answer
    recv_data, addr = client.recvfrom(4096)
    print('recv<< ', binascii.hexlify(recv_data))
    return recv_data

def set_b000_to_0(client):
    print('Set B000 to 0')
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
    data_index = "<00><00>"    # B000
    request_num = "<01>"    # fixed
    compute = "<02>"    # read: Set_Attribute_All ：0x02
    padding = "<00><00>"
    sub_header = command + data_index + request_num + compute + padding

    # data
    data = "<00>"

    # request
    ascii_str = header + sub_header + data

    # ascii code to binary
    data = ascii_to_binary(ascii_str)

    # send data
    recv_data = send_data(client, data)
    print('done')
    ### SET B000 END ###


def set_b001(df_len, client):
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
    padding = "<00><00>"
    sub_header = command + data_index + request_num + compute + padding

    # data
    data = "<" + '{:02X}'.format(df_len) + ">"   # no data for read

    # request
    ascii_str = header + sub_header + data

    # ascii code to binary
    data = ascii_to_binary(ascii_str)

    # send data
    recv_data = send_data(client, data)
    print('done')
    ### SET B001 END ###


def set_data_to_yac(dir_name, file_name, client):
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

    # use csvreader instead
    # robot coord and pulse column does not have the same column number
    with open(file_path,'r') as csvfile:
        reader = csv.reader(csvfile)
        df = list(reader)
    #df = pd.read_csv(file_path, header=None)
    ### LOAD CSV FILE END ###

    df_len = len(df)
    set_b001(df_len, client)

    ### SET P START ###
    # 1 loop is 1 line
    print('Writing position data...')
    for i in range(df_len):
        v = df[i]
        r_or_p = v[0]
        del v[0]

        v = np.array(v).astype(np.int64)
        if r_or_p == 'p':
            e = v[6]
        else:
            e = np.int64(0)

        set_position(to_ascii(np.int64(i), 2),
               to_ascii(v[0], 4), to_ascii(v[1], 4),
               to_ascii(v[2], 4), to_ascii(v[3], 4),
               to_ascii(v[4], 4), to_ascii(v[5], 4),
               to_ascii(e, 4), r_or_p)
    print('done')
    ### SET P END ###

    return True

'''
write position data to P[i]
'''
def set_position(i, x, y, z, r_x, r_y, r_z, e, r_or_p):
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
    request_num = "<00>"    # dynamic (fixed: robot coordinate value 17)
    compute = "<02>"    # dynamic: Set_Attribute_All ：0x02
    padding = "<00><00>"
    sub_header = command + data_index + request_num + compute + padding

    # data
    # robot or pulse
    if r_or_p == 'p':
        data_type = "<00><00><00><00>"  # fixed
    else:
        data_type = "<11><00><00><00>"  # fixed
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
    if r_or_p == 'p':
        coor7 = e
    else:
        coor7 = "<00><00><00><00>"  # fixed
    coor8 = "<00><00><00><00>"  # fixed
    coors = coor1 + coor2 + coor3 + coor4 + coor5 + coor6 + coor7 + coor8
    data = data_common_part + coors

    # request
    ascii_str = header + sub_header + data

    # ascii code to binary
    data = ascii_to_binary(ascii_str)

    # send data
    recv_data = send_data(client, data)


def start_job(client):
    ### START JOB START ###
    print('Start job')

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
    padding = "<00><00>"
    sub_header = command + data_index + request_num + compute + padding

    # data
    job_start = "<01><00><00><00>"    # fixed
    data = job_start

    # request
    ascii_str = header + sub_header + data

    # ascii code to binary
    data = ascii_to_binary(ascii_str)

    # send data
    recv_data = send_data(client, data)

    print('Start job done')
    ### START JOB END ###

def wait_job_complete(client):
    ### WAIT JOB COMPLETE START ###
    while True:
        print("wait for job completion")
        for wait_time in range(10): # Delay for 10s
            print('.', end='', flush=True)
            time.sleep(0.1)
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
        padding = "<00><00>"
        sub_header = command + data_index + request_num + compute + padding

        # data
        data = ""   # no data for read

        # request
        ascii_str = header + sub_header + data

        # ascii code to binary
        data = ascii_to_binary(ascii_str)

        # send data
        recv_data = send_data(client, data)

        result_flag = recv_data[-1]
        print('took ' + str(time.time() - start))

        if result_flag:
            print('complete!')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print()
            time.sleep(0.1)
            break
    ### WAIT JOB COMPLETE END ###

def servo_on(client):
    print('start')

    # header
    yerc = "<59><45><52><43>"   # fixed
    header_size = "<20><00>"    # fixed
    data_size = "<04><00>"      # dynamic (fixed: 4 for servo on/off)
    reserved1 = "<03><01><00><00>"   # fixed
    blocked = "<00><00><00><00>"    # fixed
    reserved2 = "<39><39><39><39><39><39><39><39>"  # fixed
    header = yerc + header_size + data_size + reserved1 + blocked + reserved2

    # sub header
    command = "<83><00>"
    data_index = "<02>" + "<00>"    # max: 99
    request_num = "<01>"    # fixed
    compute = "<10>"    # Set_Attribute_Single ：0x10
    padding = "<00><00>"
    sub_header = command + data_index + request_num + compute + padding

    # data
    on_off = "<01><00><00><00>"    # on: <01><00><00><00>, off: <02><00><00><00>
    data = on_off

    # request
    ascii_str = header + sub_header + data

    # ascii code to binary
    data = ascii_to_binary(ascii_str)

    # send data
    recv_data = send_data(client, data)

    print('done')


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


def ascii_to_binary(ascii_str):
    # ascii code to binary
    data = bytearray()
    matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
    for match in matches:
        data += bytearray.fromhex(match)
    return data




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
    start = time.time()
    DEFAULT_DIR = 'csv_files'
    dir_name = parser()
    print('directory name: ', dir_name)

    if dir_name is None:
        print('set default dir name', DEFAULT_DIR)
        dir_name = DEFAULT_DIR

    if not os.path.exists(dir_name):
        print('directory "', dir_name, '"not exist')
        sys.exit()

    # sorted dir list
    files = []
    for i in sorted(os.listdir(dir_name)):
        files.append(i)

    print(files)

    # init udp client
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.bind((SOURCE_ADDR, SOURCE_PORT))

    # init
    set_b000_to_0(client)
    servo_on(client)

    # check all files in the directory
    for file_name in files:
        point_set_success = set_data_to_yac(dir_name, file_name, client)
        if not point_set_success:
            continue

        start_job(client)

        print('took ' + str(time.time() - start))

        wait_job_complete(client)


