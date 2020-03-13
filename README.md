# djangoDemo

1. 安装依赖 
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt

2. 准备一个apache服务镜像,用于软件效果验证（这里也可以是一个任意web demo镜像）
```bash
cd Apache && docker build -t="apache" . && cd ..
```
准备镜像二：
```bash
git clone git@github.com:jura4x01/tictactoe-web.git
cd tictactoe-web
docker build -t tictactoe .
```


3. 启动服务 
python manage.py runserver

4. 访问地址 
http://127.0.0.1:8000

4. 启动docker容器 
在启动输入框输入apahce，点击启动（目前仅有一个测试镜像，为apache服务，启动容器需要几秒钟时间）
ps:如果需要添加其他测试镜像，请自行准备镜像，并在配置文件添加启动命令和监听端口

6. 软件验收 
网页自动跳转验证效果

7. 关闭docker容器
在停止输入框输入apahce，点击停止（停止并删除容器需要几秒到几十秒不等）

