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

def readI(client,nameStr):
    if nameStr[0]=='I' or nameStr[0]=='i':
        if nameStr[1]>='0' and nameStr[1]<='3':
            addr=int(nameStr.split('.')[0][1:])
            bit=int(nameStr.split('.')[1])
            if bit>7:
                print "I bit out of range"
                return
            m_data = client.read_area(0x81, 0, addr, 1)
            return  (struct.unpack('!B', m_data)[0]>>bit)&1
        else:
            print "input out of range"
            return

    else:
        print "input error"
        return


def readQ(client,nameStr):
    if nameStr[0]=='Q' or nameStr[0]=='q':
        if nameStr[1]>='0' and nameStr[1]<='3':
            addr=int(nameStr.split('.')[0][1:])
            bit=int(nameStr.split('.')[1])
            if bit>7:
                print "Q bit out of range"
                return
            m_data = client.read_area(0x82, 0, addr, 1)
            return  (struct.unpack('!B', m_data)[0]>>bit)&1
        else:
            print "output out of range"
            return

    else:
        print "input error"
        return 

def readM(client,nameStr):
    if nameStr[0]=='M' or nameStr[0]=='m':
        if nameStr[1]>='0' and nameStr[1]<='9':
            addr=int(nameStr.split('.')[0][1:])
            bit=int(nameStr.split('.')[1])
            if bit>7:
                print "M bit out of range"
                return
            m_data = client.read_area(0x83, 0, addr, 1)
            return  (struct.unpack('!B', m_data)[0]>>bit)&1
        elif nameStr[1]=="B" or nameStr[1]=='b':
            addr=int(nameStr[2:])
            m_data=client.read_area(0x83, 0, addr, 1)
            return struct.unpack('!b', m_data)[0]
        elif nameStr[1]=="W" or nameStr[1]=='w':
            addr=int(nameStr[2:])
            m_data=client.read_area(0x83, 0, addr, 2)
            return struct.unpack('!h', m_data)[0]
        elif nameStr[1]=="D" or nameStr[1]=='d':
            addr=int(nameStr[2:])
            m_data=client.read_area(0x83, 0, addr, 4)
            return struct.unpack('!i', m_data)[0]
            
    else:
        print "input error"
        return
if __name__ == "__main__":
    client_fd = plc_connect('192.168.1.2')
    result=readM(client_fd,"M10.4")
    print 'M10.4=',result

    result=readM(client_fd,"MB124")
    print 'MB124=',result

    result=readI(client_fd,"i1.6")
    print 'i1.6=',result

    result=readM(client_fd,"mw56")
    print 'MW56=',result

    result=readQ(client_fd,"q2.9")
    print 'q2.9=',result

    result=readM(client_fd,"md911")
    print 'MD911=',result

    plc_con_close(client_fd)