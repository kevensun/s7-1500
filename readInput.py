#coding:utf-8
import struct
import time
import snap7

def plc_connect(ip, rack=0, slot=1):
    client = snap7.client.Client()
    client.connect(ip, rack, slot)
    return client

def plc_con_close(client):
    client.disconnect()

def test_input(client):
    area = snap7.snap7types.areas.PE ##0x81
    dbnumber = 0
    size = 2
    start = 0
    result=client.read_area(area,dbnumber,start,size)
    print struct.unpack('!H',result)[0]
    InputList=[]
    for i in range(0,8*size):
        if (int(struct.unpack('!H',result)[0])& pow(2,i)!=0):
            InputList.append(1)
        else:
            InputList.append(0)
    for i in range(8*size):
        if i>=8 and i<=15:
            print 'I0.%d is %d'%(i-8,InputList[i])       
        elif i>=0 and i<=7:
            print 'I1.%d is %d'%(i,InputList[i])

# def test_input(client):
#     area = snap7.snap7types.areas.PE ##0x81
#     dbnumber = 0
#     size = 1
#     start = 0
#     result=client.read_area(area,dbnumber,start,size)
#     #print struct.unpack('!B',result)[0]
#     I0=[]
#     for i in range(0,8):
#         if (int(struct.unpack('!B',result)[0])& pow(2,i)!=0):
#             I0.append(1)
#         else:
#             I0.append(0)
#     for i in range(8):
#         print 'I0.%d is %d'%(i,I0[i])

if __name__ == "__main__":
    client_fd = plc_connect('192.168.1.2')
    test_input(client_fd)
    plc_con_close(client_fd)