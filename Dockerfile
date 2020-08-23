#所采用的基础镜像
FROM python:3.7

MAINTAINER Dalao-Li <dalaocasper@foxmail.com>

# 为镜像添加标签
LABEL version="v1" description="Docker deploy Django" by="Dalao-Li"

#程序的运行目录
WORKDIR /usr/src/nptepad

#设置时区为上海
ENV TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#导入依赖文件
COPY requirements.txt ./

#安装库
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/

# 复制项目文件
COPY . .


CMD ["gunicorn", "Notepad.wsgi", "-c", "gunicorn_config.py"]