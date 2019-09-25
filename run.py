#!/usr/bin/python2.7
import json
import requests
import socket
from wsgiref.simple_server import make_server

def paas_check(host, port):
    result = "1"
    try:
        s = socket.socket()
        s.connect((host, port))
    except Exception as e:
        print("Exception occurred: {}".format(e))
        result = "0"
    if result == "1":
        s.close()
    return result



def metrics():
    url = 'http://prometheus.product.co-mall/api/v1/query?query=probe_success'
    req = requests.post(url=url)
    project_list = json.loads(req.text)
    s=''
    for key in project_list['data']['result']:
        if 'rancher' in key['metric']['instance']:
            a = key['metric']['instance'][8:].split(".")[0]
        elif 'www.co-mall' in key['metric']['instance']:
            a = 'website'
        elif 'baidu' in key['metric']['instance']:
            continue
        elif 'jiranew' in key['metric']['instance']:
            a = 'jira_648'
        elif 'jira.product' in key['metric']['instance']:
            a = 'jira_712'
        elif 'jenkins-bj' in key['metric']['instance']:
            a = 'jenkins'
        elif 'traefik' in key['metric']['instance']:
            continue
        elif 'grafana' in key['metric']['instance']:
            continue
        elif 'harbor.product' in key['metric']['instance']:
            a = 'harbor_m'
        elif 'harbor-slave' in key['metric']['instance']:
            a = 'harbor_s'
        elif 'devopscenter' in key['metric']['instance']:
            a = 'devops'
        elif 'prometheus' in key['metric']['instance']:
            a = 'Prome'
        else:
            a = key['metric']['instance'][7:].split(".")[0]
        b = 'saas_screen{name="'+a+'"} '+key['value'][1]+'\n'
        s += b

    paaslist=[["10.90.28.51","21036","mongo_36"],["10.90.28.51","21030","mongo_30"],["10.90.28.51","21040","mongo_40"],["10.90.28.50","3356","mysql_56"],["10.90.28.50","3357","mysql_57"],["10.90.28.50","3355","mysql_55"],["10.90.26.179","80","nginx_179"],["10.90.26.5","80","nginx_265"],["10.68.46.123","9200","ES"],["172.17.2.30","53","dns_s"],["10.68.0.2","53","coredns"],["172.17.2.32","53","dns_m"],]
    for i in paaslist:
        b = 'saas_screen{name="'+i[2]+'"} '+paas_check(i[0],int(i[1]))+'\n'
        s += b
    return s



def  main():
    ip='0.0.0.0'
    port=80
    httpd =make_server(ip,port,application)
    print(metrics())
    httpd.serve_forever()
def application(environ,start_response):
    status='200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status,response_headers)
    print(metrics())
    byt=metrics().encode('utf-8')
    return [byt]

main()