import binascii
import socket
import re

if "__main__" == __name__:
    #SOURCE_ADDR = 'localhost'
    SOURCE_ADDR = '192.168.1.10'
    SOURCE_PORT = 10050 

    #DESTINATION_ADDR = 'localhost'
    DESTINATION_ADDR = '192.168.1.99'
    DESTINATION_PORT = 10040 

    df_len = 10
    

    print('start')

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
    print('sent>> ', binascii.hexlify(data));

    # answer
    # header 20 byte
    # sub header 8 byte
    # data 1 byte
    recv_data, addr = client.recvfrom(4096)
    print('recv<< ', binascii.hexlify(recv_data))

    print('done')
