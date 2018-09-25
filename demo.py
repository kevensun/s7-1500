#coding:utf-8

# 设置PLC的连接地址
ip = '192.168.1.2'  # PLC的ip地址
rack = 0  # 机架号
slot = 1  # 插槽号
tcpport = 102  # TCP端口号

import snap7
import struct


client = snap7.client.Client()
client.connect(ip, rack, slot, tcpport)

#result = client.db_read(db_number=11, start=0, size=24)
#float1, float2, word1, word2, float3, word3, word4, int = struct.unpack('!ffhhfhhi', result)

result=client.read_area(0x81,0,0,1)
inputresult= struct.unpack('!B', result)


client.write_area(0x82, 0,0,struct.pack('B',18)) 
result=client.read_area(0x82,0,0,1)

# print struct.unpack('!B',result)[0]
# Q0=[]
# for i in range(0,8):
#     if (int(struct.unpack('!B',result)[0])& pow(2,i)!=0):
#         Q0.append(1)
#     else:
#         Q0.append(0)

# for i in range(8):
#     print 'Q0.%d is %d'%(i,Q0[i]) 


result=client.db_read(1,0,4)
dbdata=struct.unpack('!f',result)[0]
print dbdata

#result = client.db_get(1)

# result=client.db_get(1)
# dbdata=struct.unpack('!B',result)
client.disconnect()
client.destroy()
