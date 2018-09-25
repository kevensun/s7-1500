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

def test_mk10_x(client):
    area = snap7.snap7types.areas.MK
    dbnumber = 0
    amount = 1
    start = 10
    bit = 3
    print  'init value'
    mk_data = client.read_area(area, dbnumber, start, amount)
    print struct.unpack('!B', mk_data)

    print   'set 1'
    client.write_area(area, dbnumber, start, struct.pack('B',pow(2,bit)))
    print   'current value'
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print   struct.unpack('!B', mk_cur)[0]>>bit

def test_mk_w201(client):
    area = snap7.snap7types.areas.MK
    dbnumber = 0
    amount = 2
    start = 201
    print   'init value'
    mk_data = client.read_area(area, dbnumber, start, amount)
    print  struct.unpack('!h', mk_data)

    print  'set 12'
    #client.write_area(area, dbnumber, start, b'\x00\x0C')
    client.write_area(area, dbnumber, start, struct.pack('!H',12))
    print    'current value'
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print   struct.unpack('!h', mk_cur)

    time.sleep(3)
    print   'set 3'
    client.write_area(area, dbnumber, start, struct.pack('!H',3))
    print   'current value'
    mk_cur = client.read_area(area, dbnumber, start, amount)
    print   struct.unpack('!h', mk_cur)

if __name__ == "__main__":
    client_fd = plc_connect('192.168.1.2')
    test_mk10_x(client_fd)
    test_mk_w201(client_fd)
    plc_con_close(client_fd)