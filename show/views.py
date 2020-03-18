from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse  
import os
import sys
import time
from subprocess import Popen, PIPE
from configparser import ConfigParser
import time
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from functools import wraps
import ipfshttpclient
sys.path.append('sdk')
from client.bcosclient import (
    BcosClient,
    BcosError
)
from client.datatype_parser import DatatypeParser

cp = ConfigParser()
cp.read("./show/config.ini")
# 获取mysql中的host值
contract_addr = cp.get("contract", 'addr')
client = BcosClient()
#从文件加载abi定义
abi_file  ="sdk/contracts/SoftwareTransaction.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

# Create your views here.
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.user.is_authenticated:
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner


def log_in(request):
    # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if not user:
            return HttpResponse("账户名或密码错误")
        auth.login(request, user)
        return redirect('/index/')
    # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request,'login.html')

def log_out(request):
    auth.logout(request)
    return redirect("/login/")

def index(request):
    return render(request, 'index.html')

@check_login
def publish(request):
    return render(request, "publish.html")

@check_login
def upload(req):
    myfile = req.FILES.get("upload", None)
    if not myfile:
        return HttpResponse("no file selected")
    if myfile.name != "Dockerfile":
        return HttpResponse("仅支持Dockerfile文件")
    newfile = open(myfile.name, 'wb+')
    for chunk in myfile.chunks():
        newfile.write(chunk)
    newfile.close()
    print("filename:", myfile.name)
    os.system("docker cp {} ipfs_host:/".format(myfile.name))
    ipfs_api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    res = ipfs_api.add(myfile.name)
    print("res:", res)
    ipfs_api.close()
    os.remove(myfile.name)
    name = req.POST.get('name')
    price = req.POST.get('price')
    args = [name.encode('utf8'), int(price), res['Hash']]
    receipt = client.sendRawTransactionGetReceipt(contract_addr, contract_abi,"publish",args)
    if receipt['status'] != '0x0':
        return render(req, "response.html", {"response":"软件发布失败"})

    txhash = receipt['transactionHash']
    return render(req, "response.html", {"response":"upload success!", "info1":"ipfs hash is {}".format(res['Hash']), "info2":"tx hash on fisco is {}".format(txhash)})

@check_login
def verify(request):
    return render(request, "verify.html")

@check_login
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

@check_login
def stop(request):
    res = ""
    software_name = request.GET.get('name')
    os.system("docker stop " + software_name)
    os.system("docker rm " + software_name)
    res = "stop ok"
    return HttpResponse(res + " at " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

@check_login
def score(request):
    name = request.POST.get('name')
    score=request.POST.get('score')
    args = [name.encode('utf8'), int(score)]
    receipt = client.sendRawTransactionGetReceipt(contract_addr, contract_abi,"varify",args)
    if receipt['status'] != '0x0':
        return render(request, "response.html", {"response":"软件不存在"})
    txhash = receipt['transactionHash']

    return render(request, "response.html", {"response":"grade success！", "info1":"tx hash on fisco is {}".format(txhash)})


@check_login
def buy(request):
    if request.method == "POST":
        name = request.POST.get('name')
        submit_name = request.POST.get("submit_name")
        if submit_name == '查询价格':
            args = [name.encode('utf8')]
            receipt = client.sendRawTransactionGetReceipt(contract_addr, contract_abi,"getPrice",args)
            if receipt['status'] != '0x0':
                return render(request, "response.html", {"response":"软件不存在"})
            res = client.call(contract_addr, contract_abi, "getPrice",[name.encode('utf8')])
            return render(request, "buy.html", {"price":res[0]})
        elif submit_name == '购买软件':
            args = [name.encode('utf8')]
            receipt = client.sendRawTransactionGetReceipt(contract_addr, contract_abi,"buySoftware",args)
            print("receipt:", receipt)
            if receipt['status'] != '0x0':
                return render(request, "response.html", {"response":"软件不存在"})
            print("contratc_addr:", contract_addr)
            res = client.call(contract_addr, contract_abi, "buySoftware",[name.encode('utf8')])
            print("res0:", res, receipt, "name:", name)
            #os.remove(res[0])
            ipfs_api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
            ipfs_api.get(res[0])
            ipfs_api.close()
            file=open(res[0],'rb')  
            response =FileResponse(file)  
            response['Content-Type']='application/octet-stream'  
            response['Content-Disposition']='attachment;filename="Dockerfile"'  
            return response 
            #return render(request, "response.html", {"response":"buy success!", "info1":"hash on ipfs is {}".format(txhash)})

    return render(request, "buy.html")