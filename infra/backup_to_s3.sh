#!/usr/bin/env bash

cd /home/ec2-user/watson/
source .venv/bin/activate
PYTHONPATH=${PYTHONPATH}:. python data/backup_db.py
