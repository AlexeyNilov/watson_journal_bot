"""
https://github.com/Doist/todoist-api-python
https://developer.todoist.com/rest/v2/?python#updating-a-task
"""

from todoist_api_python.api_async import TodoistAPIAsync
from conf.settings import TDIST_API_TOKEN

CLIENT = TodoistAPIAsync(TDIST_API_TOKEN)


async def add_task(content: str):
    content = content.strip()
    due_string = None
    priority = 1
    if ".urg" in content:
        priority += 1
        content = content.replace(".urg", "")
    if ".imp" in content:
        priority += 1
        content = content.replace(".imp", "")
    if ".today" in content:
        priority += 1
        due_string = "Today"
        content = content.replace(".today", "")
    content = content.strip()
    await CLIENT.add_task(
        content=content,
        labels=["from_watson"],
        priority=priority,
        due_string=due_string,
    )
