from django.shortcuts import render
from django.http import HttpResponse
import os
import sys
import time
from subprocess import Popen, PIPE
from configparser import ConfigParser
import time

# Create your views here.
# Create your views here.
def index(request):
    return render(request, 'index.html')

def start(request):
    res = ""
    software_name = request.GET.get('name')
    cp = ConfigParser()
    # 以.ini结尾的配置文件
    cp.read("./show/config.ini")

    # 获取mysql中的host值
    cmd = cp.get(software_name, 'cmd')
    port = cp.get(software_name, 'port')
    print("cmd:", cmd, "port:", port)
    if len(cmd) != 0 and len(port) != 0:
        child = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = child.communicate()
        ret = child.wait()
        if len(err) != 0:
            res = "container " + software_name + " has been running"
        else:
            res = ("http://localhost:{}\n" + "start ok").format(port)
            time.sleep(5)
    else:
        res = "software not found:" + software_name
    return HttpResponse(res + " at " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

def stop(request):
    res = ""
    software_name = request.GET.get('name')
    os.system("docker stop " + software_name)
    os.system("docker rm " + software_name)
    res = "stop ok"
    return HttpResponse(res + " at " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
