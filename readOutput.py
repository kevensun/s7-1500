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

def test_output(client):
    area = snap7.snap7types.areas.PA ##0x82
    dbnumber = 0
    size = 1
    start = 0
    result=client.read_area(area,dbnumber,start,size)
    Q0=[]
    for i in range(0,8):
        if (int(struct.unpack('!B',result)[0])& pow(2,i)!=0):
            Q0.append(1)
        else:
            Q0.append(0)
    for i in range(8):
        print 'Q0.%d is %d'%(i,Q0[i])

if __name__ == "__main__":
    client_fd = plc_connect('192.168.1.2')
    test_output(client_fd)
    #print client_fd.get_connected()
    #print client_fd.get_cpu_state()
    plc_con_close(client_fd)