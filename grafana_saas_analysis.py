import json
import requests
from wsgiref.simple_server import make_server


def creat_project():
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
        else:
            a = key['metric']['instance'][7:].split(".")[0]
        b = 'saas_screen{name="'+a+'"} '+key['value'][1]+'\n'
        s += b
    return s


def  main():
    ip='0.0.0.0'
    port=80
    httpd =make_server(ip,port,application)
    print(creat_project())
    httpd.serve_forever()
def application(environ,start_response):
    status='200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status,response_headers)
    print(creat_project())
    byt=creat_project().encode('utf-8')
    return [byt]

main()