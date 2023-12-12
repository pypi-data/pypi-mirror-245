# 建立 python3.7 环境 https://blog.csdn.net/weixin_42134789/article/details/106345938
FROM python:3.9
# 镜像作者cx
MAINTAINER cx
# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
COPY pip.conf /root/.pip/pip.conf
# 创建 tsa 文件夹
RUN mkdir -p /hbyapp/sobase
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
# 将 tsa 文件夹为工作目录
WORKDIR /hbyapp/sobase
# 将当前目录加入到工作目录中（. 表示当前目录）
ADD . /hbyapp/sobase

# supervisor
RUN mkdir -p /var/log/supervisor \
    &&  mkdir -p /var/log/sobase
RUN touch /var/run/supervisor.sock
RUN chmod 777 /var/run/supervisor.sock
COPY compose/supervisor/supervisord.conf /etc/supervisord.conf
COPY compose/supervisor/master-celery.conf /etc/supervisor/conf.d/master-celery.conf
COPY compose/supervisor/websocket-base.conf /etc/supervisor/conf.d/websocket-base.conf
# 更新pip版本
RUN /usr/local/bin/python -m pip install --upgrade pip

# 利用 pip 安装依赖
RUN pip install -r requirements.txt
#RUN pip download -d packages -r requirements.txt
#RUN pip install --no-index --find-links=packages -r requirements.txt
# 去除windows系统编辑文件中多余的\r回车空格
RUN sed -i 's/\r//' ./start.sh
# 给资源文件夹授权
RUN chmod -R 777 /hbyapp/sobase/media/
RUN chmod -R 777 /hbyapp/sobase/logs/
RUN chmod -R 777 /var/log/
# 给start.sh可执行权限
RUN chmod +x ./start.sh

# 数据迁移，并使用uwsgi启动服务
# ENTRYPOINT /bin/bash ./start.sh
# "supervisord","-c","/etc/supervisord.conf" supervisord -c /etc/supervisord.conf
# ENTRYPOINT ["/usr/local/bin/supervisord","-n","-c","/etc/supervisord.conf"]
CMD ["./start.sh"]