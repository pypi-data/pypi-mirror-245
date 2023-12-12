#coding:utf-8

import os, sys
import datetime as dt
import traceback
import json

from . import xtbson as bson

### connection

__client = None
__client_last_spec = ('', None)


def connect(ip = '', port = None, remember_if_success = True):
    global __client

    if __client:
        if __client.is_connected():
            return __client

        __client.shutdown()
        __client = None

    from . import xtconn

    if not ip:
        ip = 'localhost'

    if port:
        server_list = [f'{ip}:{port}']
        __client = xtconn.connect_any(server_list)
    else:
        server_list = xtconn.scan_available_server()

        default_addr = 'localhost:58610'
        if not default_addr in server_list:
            server_list.append(default_addr)

        __client = xtconn.connect_any(server_list)

    if not __client or not __client.is_connected():
        raise Exception("无法连接xtquant服务，请检查QMT-投研版或QMT-极简版是否开启")

    if remember_if_success:
        global __client_last_spec
        __client_last_spec = (ip, port)

    return __client


def reconnect(ip = '', port = None, remember_if_success = True):
    global __client

    if __client:
        __client.shutdown()
        __client = None

    return connect(ip, port, remember_if_success)


def get_client():
    global __client

    if not __client or not __client.is_connected():
        global __client_last_spec

        ip, port = __client_last_spec
        __client = connect(ip, port, False)

    return __client


### utils
def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            message = '\n{0} raise {1}:{2}'.format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
            # raise exc_type(message)
            print(message)
            return None

    return wrapper

def __bsoncall_common(interface, func, param):
    return bson.BSON.decode(interface(func, bson.BSON.encode(param)))

def create_view(viewID, view_type, title, group_id):
    client = get_client()
    return client.createView(viewID, view_type, title, group_id)

#def reset_view(viewID):
#    return

def close_view(viewID):
    client = get_client()
    return client.closeView(viewID)

#def set_view_index(viewID, datas):
#    '''
#    设置模型指标属性
#    index: { "output1": { "datatype": se::OutputDataType } }
#    '''
#    client = get_client()
#    return client.setViewIndex(viewID, datas)

def push_view_data(viewID, datas):
    '''
    推送模型结果数据
    datas: { "timetags: [t1, t2, ...], "outputs": { "output1": [value1, value2, ...], ... }, "overwrite": "full/increase" }
    '''
    client = get_client()
    bresult = client.pushViewData(viewID, 'index', bson.BSON.encode(datas))
    return bson.BSON.decode(bresult)

def switch_graph_view(stock_code = None, period = None, dividendtype = None, graphtype = None):
    cl = get_client()

    result = __bsoncall_common(
        cl.commonControl, 'switchgraphview'
        , {
            "stockcode": stock_code
            , "period": period
            , "dividendtype": dividendtype
            , "graphtype": graphtype
        }
    )


def push_xtview_data(data_type, time, datas):
    cl = get_client()
    timeData = 0
    types = []
    numericDatas = []
    stringDatas = []
    if type(time) == int:
        name_list = list(datas.keys())
        value_list = []
        for name in name_list:
            value_list.append([datas[name]])
        timeData = [time]
    if type(time) == list:
        time_list = time
        name_list = list(datas.keys())
        value_list = list(datas.values())
        timeData = time_list

    for value in value_list:
        if isinstance(value[0], str):
            stringDatas.append(value)
            types.append(3)
        else:
            numericDatas.append(value)
            types.append(0)

    result = __bsoncall_common(
        cl.custom_data_control, 'pushxtviewdata'
        , {
            'dataType': data_type
            ,'timetags': timeData
            , 'names' : name_list
            , 'types' : types
            , 'numericDatas' : numericDatas
            , 'stringDatas' : stringDatas
        }
    )
    return

