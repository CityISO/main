#!/usr/bin/env bash

BASE_DIR=/home/denissurkov/projects/city_iso_project/main/

source ${BASE_DIR}/venv/bin/activate
gunicorn -w 2 --log-file data.log -b 127.0.0.1:8000 city_iso.wsgi:application
