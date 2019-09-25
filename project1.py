import socket               # 导入 socket 模块
import json
import requests
from wsgiref.simple_server import make_server
 
def connect(host,port):
    try:
        s = socket.socket()         # 创建 socket 对象
        s.connect((host, port))
    
    except socket.error,msg: 
        if 'Connection refused' in msg:
            return 'failed'
        else:
            print(msg)
    else:
        s.close()
        return 'success'

def tcp_test():
    scheduler = 10251
    controller = 10252
    etcd = 2379
    master_ip = ['10.239.160.11','10.239.160.12','10.239.160.13']
    etcd_ip = ['10.239.160.15','10.239.160.16','10.239.160.17']
    
    value = '1'
    for ip in master_ip:
        if connect(ip,scheduler) == 'failed':
            value = '0'
            break
    result = 'cluster_health{job="scheduler"} '+value+'\n'

    value = '1'
    for ip in master_ip:
        if connect(ip,controller) == 'failed':
            value = '0'
            break
    result += 'cluster_health{job="controller"} '+value+'\n'

    for ip in etcd_ip:
        if connect(ip,etcd) == 'success':
            result += 'cluster_health{job="etcd_'+ip.split('.')[3]+'"} 1\n'
        else:
            result += 'cluster_health{job="etcd_'+ip.split('.')[3]+'"} 0\n'
    return result


def  main():
    ip='0.0.0.0'
    port=80
    httpd =make_server(ip,port,application)
    print(tcp_test())
    httpd.serve_forever()
def application(environ,start_response):
    status='200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status,response_headers)
    print(tcp_test())
    byt=tcp_test().encode('utf-8')
    return [byt]

main()