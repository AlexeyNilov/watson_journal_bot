#!/usr/bin/env bash

cd /home/ec2-user/watson_journal_bot/
export LOG_LEVEL="ERROR"
export PYTHONPATH=${PYTHONPATH}:.
source .venv/bin/activate
python bot/watson.py
