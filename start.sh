#!/usr/bin/env bash
# linux下，运行/重启程序
pkill gunicorn
rm SnailApp.pid
./venv/bin/gunicorn --config gunicorn.conf -k gevent manage:app --reload