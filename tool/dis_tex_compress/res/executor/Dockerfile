FROM python:3.6.15-slim-bullseye

WORKDIR /app

COPY bin bin
COPY common common
COPY config config
COPY lib lib
COPY log log
COPY logic logic
COPY main_frame main_frame
COPY res res
COPY __init__.py __init__.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD ["python", "main_frame/main.py", "executor_k8s", "data"]
