import dolphindb as ddb


def connect(url,port, userid='admin', passwd='123456'):
    s = ddb.session()
    s.connect(url, port, userid=userid, password=passwd)
    return s


def close_ddb(s):
    s.close()
