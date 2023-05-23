# 使用官方 Python 基础镜像
FROM python:3.8-slim-buster

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录中的内容复制到 /app 中
COPY . /app

# 安装应用程序所需的依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露容器的端口
EXPOSE 5000

# 定义环境变量
ENV FLASK_APP=app.py

# 在容器启动时运行应用程序
CMD ["flask", "run", "--host=0.0.0.0"]
