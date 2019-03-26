#!/usr/bin/env bash

BASE_DIR=/home/denissurkov/projects/city_iso_project/main/

source ${BASE_DIR}/venv/bin/activate

celery -A city_iso.celery:app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler