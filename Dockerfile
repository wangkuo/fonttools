FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p /app/fonts

# 设置环境变量
ENV FLASK_SECRET_KEY=your-production-secret-key

COPY requirements.txt .
# 使用清华源安装依赖
#RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r requirements.txt
RUN pip install -r requirements.txt

COPY . .

VOLUME /app/fonts

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000","--timeout", "60", "app.wsgi:app"] 