FROM python:2.7.18-slim-buster AS base

RUN apt update && \
    apt install -y bluez

RUN pip install -U pip && pip install pexpect

WORKDIR /app
COPY desay_dfu.py ./

ENTRYPOINT [ "python", "./desay_dfu.py"]