# Repository Structure

## bot/
Contains the main bot logic:
- `watson.py`: The main bot implementation with various commands and handlers
- `command.py`: Command handlers for the bot
- `conversation.py`: Conversation handlers for the bot
- `message.py`: Message handlers for the bot
- `common.py`: Utility functions for the bot

## conf/
Configuration files:
- `settings.py.sample`: Sample configuration file (actual `settings.py` is gitignored)

## data/
Data-related functionality:
- `fastlite_db.py`: Database setup and table definitions using FastLite
- `logger.py`: Logging configuration
- `backup_db.py`: Database backup functionality
- `generate_schema.py`: Script to generate database schemas
- `migrate_db.py`: Database migration script
- `view_db.py`: Script to view database contents
- `schema.sql`: SQL schema for the database

## db/
Database and data files:
- `watson.sqlite`: SQL database

## doc/
Documentation files:
- `repo.md`: Repository structure
- `user_story.md`: User stories and feature ideas

## infra/
Infrastructure and deployment-related files:
- `start_bot.sh`: Script to start the bot
- `github_syncer.sh`: Script to sync code from GitHub
- `backup_to_s3.sh`: Script to backup the database to S3
- Various systemd service and timer files for automating processes

## model/
Data models:

## sample/
Sample scripts:

## service/
Business logic and services:
- `repo.py`: Repository pattern implementation for data access

## test/
Unit tests
