# 软件交易系统

### 说明：
本项目依赖于fisco区块链以及ipfs，并基于django2.1实现，因此首先需要启动fisco节点和ipfs节点

### 安装依赖

##### 安装并启动fisco节点
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

//将证书文件拷贝到software/bin目录和software/sdk/bin目录下
cp ~/fisco/nodes/127.0.0.1/sdk/* ~/software/bin/
cp ~/fisco/nodes/127.0.0.1/sdk/* ~/software/sdk/bin/
```
更多详情参考 https://github.com/FISCO-BCOS/python-sdk

##### 拉取docker镜像，启动一个ipfs服务
```
//拉取镜像
docker pull ipfs/go-ipfs
//启动容器
docker run -d --name ipfs_host -p 4001:4001 -p 127.0.0.1:8181:8181 -p 127.0.0.1:5001:5001 ipfs/go-ipfs:latest
```

##### 以下操作默认用户当前处于项目根目录software下

##### 准备两个测试用镜像，用于软件效果验证
```bash
cd apache && docker build -t=apache . && cd ..
cd tictactoe && docker build -t=tictactoe . && cd ..
```

##### 安装python依赖库

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt
cd sdk && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt && cd ..
```

##### 部署合约并配置合约地址
cd sdk && python deploy.py
//脚本会返回新部署的合约地址，复制该合约地址，粘贴到show/config.ini文件


### 操作流程

1. 启动服务 
python manage.py runserver

2. 访问地址 
http://127.0.0.1:8000
首页提供三个操作
 * 发布软件
 * 验证软件
 * 购买软件
执行任何操作都需要登录，未登录会自动跳转到登录界面
本项目提供三个测试账号
developer、third-party、buyer
密码均为123456

3. 发布软件时仅支持上传Dockerfile文件，可以用tictactoe/Dockerfile文件测试，软件名为tictactoe
验证软件网页也需要登录，登录时可以用任意账号登录

4. 用户购买软件之后下载一个Dockerfile文件，切换到Dockerfile所在目录，执行
```
docker build -t=tictactoe . && docker run -d --name=tictactoe --net=host tictactoe
```
即可本地运行所购软件，运行软件可以基于任何已经安装过docker的操作系统

5. fisco 查询交易记录
sdk目录下执行：
python console.py getTransactionReceipt 0x98ccea0432d5194e5998e2f6667d65606c4048a4a64ed290d3c478631023c652
或
python console.py getTransactionByHash 0x98ccea0432d5194e5998e2f6667d65606c4048a4a64ed290d3c478631023c652

### 注意事项
1. 买家初始余额为10000， 其他人初始余额为0
2. 第三方验证收费固定为50，因此买家预存入的押金为软件初始价格+50，因此若软甲价格高于9950会导致买家余额不足。建议软件价格远低于10000
