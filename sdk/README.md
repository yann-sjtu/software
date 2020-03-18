# 软件交易系统

## 项目说明
1. 本项目基于fisco项目的python-sdk二次开发完成
2. 本项目需要首先运行fisco节点和ipfs节点
3. 本项目需要运行一个软件验证服务，项目地址：https://github.com/yann-sjtu/software
4. 请使用python3运行

## 使用步骤

1. 安装并启动fisco节点，可以参考官方教程 
```bash
//创建节点目录
cd ~ && mkdir -p fisco && cd fisco
//下载build_chain.sh脚本
curl -LO https://github.com/FISCO-BCOS/FISCO-BCOS/releases/download/v2.2.0/build_chain.sh && chmod u+x build_chain.sh
//在fisco目录下执行下面的指令，生成一条单群组4节点的FISCO链。请确保机器的30300~30303，20200~20203，8545~8548端口没有被占用。
bash build_chain.sh -l "127.0.0.1:4" -p 30300,20200,8545
//启动所有节点
bash nodes/127.0.0.1/start_all.sh
//启动成功会输出类似下面内容的响应
# try to start node0
# try to start node1
# try to start node2
# try to start node3
#  node1 start successfully
#  node2 start successfully
#  node0 start successfully
#  node3 start successfully
```
更多详情参考 https://github.com/FISCO-BCOS/python-sdk 

2. 安装docker，拉取ipfs镜像并启动一个ipfs容器
```
//拉取镜像
docker pull ipfs/go-ipfs
//启动容器(为方便操作ipfs上传文件，最好把本地的项目路径映射到容器内,-v后的参数修改为自己的路径)
docker run -d --name ipfs_host -p 4001:4001 -p 127.0.0.1:8181:8181 -p 127.0.0.1:5001:5001 ipfs/go-ipfs:latest
```
3. 启动项目验证服务，具体操作参考 https://github.com/yann-sjtu/software

4. 安装依赖
$ pip install -r requirements.txt
如果提示权限问题，可以在后面加 --user 

5. 拷贝整数到python-sdk/bin目录
`cp ~/fisco/nodes/127.0.0.1/sdk/* bin/`

6. 启动脚本
`python demo_software.py`

## 软件交易合约说明
本合约主要提供四个接口：
  1. publish
  开发者首先将软件源代码上传至ipfs，然后通过该接口发布软件，包括软件名、软件价格以及软件在ipfs上的哈希值
  2. varify
  官方验证软件效果，并为软件背书，并开放软件交易（若软件没有第三方背书则无法进行交易）
  2. getPrice
  买家查询软件的价格
  3. buySoftware
  买家付款，付款成功合约会返回软件在ipfs上的哈希值

示例软件路径为/home/yann/python-sdk/Dockerfile
软件名为apache
软件价格任意