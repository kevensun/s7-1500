import snap7.client
from snap7.snap7types import *
from snap7.util import *
import sys
# offsets = { "Bool":2,"Int": 2,"Real":4,"DInt":6,"String":256} 

# db=\
# """
# a    Real   0.0
# b    Bool   4.0
# c    Int    6.0
# d   String  8.0
# e    Int    264.0

# """
# 
def DBRead(fd,str_db_num,str_type,str_offset):
    if str_db_num[:2] == 'DB' or str_db_num[:2] == 'db':
        db_num=int(str_db_num[2:])
        data = plc.read_area(areas['DB'],db_num,0,266)#最大读266，试出来的
        if str_type == 'Real':
            offset = int(str_offset.split('.')[0])
            value = get_real(data,offset)
            return value
        if str_type == 'Bool':
            offset = int(str_offset.split('.')[0])
            bit = int(str_offset.split('.')[1])
            if bit >7:
                print "bit out of range"
                sys.exit(0)
            else:
                value = get_bool(data,offset,bit)
                return value
        if str_type == 'Int':
            offset = int(str_offset.split('.')[0])
            value = get_int(data,offset)
            return value
        if str_type == 'String':
            offset = int(str_offset.split('.')[0])
            value = get_string(data, offset,266)
            return value         
    else:
        print "input error"
        sys.exit(0)


if __name__ == "__main__":
    plc = snap7.client.Client()
    plc.connect('192.168.1.2',0,1)

    result=DBRead(plc,"db1","Real","0.0")
    print result

    result=DBRead(plc,"db1","Bool","4.0")
    print result

    result=DBRead(plc,"db1","Int","6.0")
    print result

    result=DBRead(plc,"DB1","Int","264.0")
    print result

    result=DBRead(plc,"db1","String","8.0")
    print result

    data=plc.db_read(1,0,4)
    result = struct.unpack('!f',data)
    print result
    
    plc.disconnect()