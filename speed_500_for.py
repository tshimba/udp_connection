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

    print('start')

    for count in range(100):

        # header
        yerc = "<59><45><52><43>"   # fixed
        header_size = "<20><00>"    # fixed
        data_size = "<02><00>"      # dynamic (fixed: 2 byte for speed)
        reserved1 = "<03><01><00><00>"   # fixed
        blocked = "<00><00><00><00>"    # fixed
        reserved2 = "<39><39><39><39><39><39><39><39>"  # fixed
        header = yerc + header_size + data_size + reserved1 + blocked + reserved2

        # sub header
        command = "<7B><00>"
        data_index = "<" + '{:02X}'.format(count) + ">" + "<00>"    # max: 99
        request_num = "<01>"    # fixed
        compute = "<02>"    # Set_Attribute_All ：0x02
        padding = "<00><00>"
        sub_header = command + data_index + request_num + compute + padding

        # data
        speed_value = "<F4><01>"    # 500: <F4><01>
        data = speed_value

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
