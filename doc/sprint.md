# Current Sprint

## Make tasks flow work

* Integrate with Todoist and sort out incoming tasks from Watson
https://github.com/Doist/todoist-api-python
https://developer.todoist.com/rest/v2/?python#updating-a-task

* Use LLM to sort the tasks by:
1. time estimate (less 5 minutes or more)
2. importance
3. urgency

* Refactor todoist structure, remove info message, leave only clear actions

## Bugs

* check for empty update text
* check this warning

Oct 20 07:00:08 ip-172-31-42-22.eu-north-1.compute.internal bash[466499]: /home/ec2-user/watson_journal_bot/bot/watson.py:38: PTBUserWarning: If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message. Read this FAQ entry to learn more about the per_* settings: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#what-do-the-per_-settings-in-conversationhandler-do.
