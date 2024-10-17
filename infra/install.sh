#!/usr/bin/env bash

# cd /home/ec2-user/
# git clone https://github.com/AlexeyNilov/watson_journal_bot.git

cd /home/ec2-user/watson_journal_bot
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp conf/settings.py.sample conf/settings.py

sudo cp -f infra/watson_bot.service /etc/systemd/system/
sudo cp -f infra/github_syncer_watson.timer /etc/systemd/system/
sudo cp -f infra/github_syncer_watson.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable github_syncer_watson.service
sudo systemctl enable github_syncer_watson.timer
sudo systemctl enable watson_bot.service
sudo systemctl start watson_bot.service
