import binascii
import socket;


import re

if "__main__" == __name__:
    #SOURCE_ADDR = 'localhost'
    SOURCE_ADDR = '192.168.1.10'
    SOURCE_PORT = 10050 

    #DESTINATION_ADDR = 'localhost'
    DESTINATION_ADDR = '192.168.1.99'
    DESTINATION_PORT = 10040 

    print('start connect');
    #client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    #client.bind(('localhost', SOURCE_PORT))
    #client.connect((DESTINATION_ADDR, DESTINATION_PORT));


    # speed 500
    #ascii_str = "<59><45><52><43><20><00><16><00><03><01><00><00><00><00><00><00><39><39><39><39><39><39><39><39><03><03><00><00><00><34><00><00><09><00><00><00><F4><01><F4><01><F4><01><F4><01><F4><01><F4><01><F4><01><F4><01><F4><01>"
    #ascii_str = "<59><45><52><43><20><00><16><00><03><01><00><00><00><00><00><00><39><39><39><39><39><39><39><39><03><03><00><00><00><34><00><00><09><00><00><00><f4><01><f4><01><f4><01><f4><01><f4><01><f4><01><f4><01><f4><01><f4><01>"
    #ascii_str = "<59><45><52><43><20><00><00><00><03><01><01><01><00><00><00><80><39><39><39><39><39><39><39><39><90><00><00><00><00><00><00><00>"

    # servo on
    #ascii_str = "<59><45><52><43><20><00><04><00><03><01><00><01><00><00><00><00><39><39><39><39><39><39><39><39><83><00><02><00><01><10><00><00><01><00><00><00>"
    #servo_on =   "<59><45><52><43><20><00><04><00><03><01><00><00><00><00><00><00><39><39><39><39><39><39><39><39><83><00><02><00><01><10><00><00><01><00><00><00>"

    #ascii_str_raw = "5945524320000000030101010000008039393939393939399000000000000000"

    # point
    #ascii_str = "<59><45><52><43>
    # <20><00><D8><01>
    # <03><01><00><00><00><00><00><00><39><39><39><39><39><39><39><39><07><03><00><00><00><34><00><00><09><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><4E><55><01><00><60><A5><FF><FF><65><E4><FF><FF><88><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><4E><55><01><00><60><A5><FF><FF><47><99><FF><FF><88><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><4E><55><01><00><76><07><00><00><47><99><FF><FF><87><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><4E><55><01><00><77><07><00><00><EF><DB><FF><FF><87><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><18><16><01><00><77><07><00><00><F0><DB><FF><FF><87><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><18><16><01><00><CB><C5><FF><FF><EF><DB><FF><FF><87><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><66><DA><00><00><CB><C5><FF><FF><ED><DB><FF><FF><87><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><6A><9F><00><00><CB><C5><FF><FF><ED><DB><FF><FF><87><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><03><66><00><00><CB><C5><FF><FF><ED><DB><FF><FF><87><0D><00><00><45><90><FF><FF><68><F2><FF><FF><50><EB><FF><FF><00><00><00><00>"
    P000 =  "<59><45><52><43><20><00><34><00><03><01><00><00><00><00><00><00><39><39><39><39><39><39><39><39><7F><00><00><00><00><02><00><00><11><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00>"
    
    ascii_str = P000

    #ascii_str = binascii.unhexlify(ascii_str_raw)


    data = bytearray()
    matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
    for match in matches:
        data += bytearray.fromhex(match)

    print(data)

    #my_hexadata = "5945524320000000030101010000008039393939393939399000000000000000"
    #scale = 16 ## equals to hexadecimal
    #num_of_bits = 8
    #bin(int(my_hexdata, scale))[2:].zfill(num_of_bits)

    #print(ascii_str)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client.bind((SOURCE_ADDR, SOURCE_PORT))
    #client.connect((DESTINATION_ADDR, DESTINATION_PORT));
    #client.sendto(bytes(ascii_str, "utf-8"), (DESTINATION_ADDR, DESTINATION_PORT))
    client.sendto(data, (DESTINATION_ADDR, DESTINATION_PORT))
    #client.sendto(ascii_str, (DESTINATION_ADDR, DESTINATION_PORT))

    #client.send(ascii_str)
    print('sent')

    data, addr = client.recvfrom(4096)
    print(data)

    #client.close();
    #print('end of connect');


