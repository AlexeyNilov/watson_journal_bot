#!/usr/bin/env bash

cd /home/ec2-user/watson/
git fetch origin

# Get the status of local vs remote
LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main)
BASE_COMMIT=$(git merge-base HEAD origin/main)

if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
    echo "The local repository is up to date with the remote repository"
elif [ "$LOCAL_COMMIT" = "$BASE_COMMIT" ]; then
    echo "The local repository is behind the remote repository"
    echo "Starting update"
    git pull
    source .venv/bin/activate
    pip install -r requirements.txt
    PYTHONPATH=${PYTHONPATH}:. python data/migrate_db.py
    sudo systemctl restart watson_bot.service
fi
