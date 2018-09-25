import snap7.client
from snap7.snap7types import *
from snap7.util import *


class DBObject(object):
    pass


offsets = { "Bool":2,"Int": 2,"Real":4,"DInt":6,"String":256} #这个不要动，我也不知道为啥

#以下面这种格式提供参数：变量名+空格+偏移量(带小数点的)+回车下一个 
db=\
"""
a    Real   0.0
b    Bool   4.0
c    Int    6.0
d   String  8.0
e    Int    264.0

"""

def DBRead(plc,db_num,length,dbitems):
    data = plc.read_area(areas['DB'],db_num,0,length)
    obj = DBObject()
    for item in dbitems:
        value = None
        offset = int(item['bytebit'].split('.')[0])
        print offset
        if item['datatype']=='Real':
            value = get_real(data,offset)

        if item['datatype']=='Bool':
            bit =int(item['bytebit'].split('.')[1])
            value = get_bool(data,offset,bit)

        if item['datatype']=='Int':
            value = get_int(data, offset)

        if item['datatype']=='String':
            value = get_string(data, offset,256)

        obj.__setattr__(item['name'], value)
        print item['name'],value

    return obj

def get_db_size(array,bytekey,datatypekey):
    seq,length = [x[bytekey] for x in array],[x[datatypekey] for x in array]
    seq1=[float(i) for i in seq]
    idx = seq1.index(max(seq1))
    lastByte = int(seq[idx].split('.')[0])+(offsets[length[idx]])
    return lastByte
def get_items(db):
    items=[]
    itemlist = filter(lambda a: a!='',db.split('\n'))
    items = [
        {
            "name":x.split()[0],
            "datatype":x.split()[1],
            "bytebit":x.split()[2]
         } for x in itemlist
    ]
    return items


if __name__ == "__main__":
    plc = snap7.client.Client()
    plc.connect('192.168.1.2',0,1)
    items = get_items(db)
    length = get_db_size(items,'bytebit','datatype')
    print "length=",length
    meh = DBRead(plc,1,length,items)
    print """
    a:\t{}
    b:\t{}
    c:\t{}
    d:\t{}
    e:\t{}
    """.format(meh.a,meh.b,meh.c,meh.d,meh.e)

    # data = plc.read_area(areas['DB'],1,0,256)
    # value = get_real(data,0)
    # print value

    # value = get_bool(data,4,0)
    # print value

    # value = get_int(data, 6)
    # print value 

    # value = get_string(data, 8,256)
    # print value


    plc.disconnect()