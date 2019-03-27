#!/usr/bin/env bash

BASE_DIR=/home/denissurkov/projects/city_iso_project/main/

source ${BASE_DIR}/venv/bin/activate

celery worker -A city_iso.celery:app
