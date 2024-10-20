"""
https://github.com/Doist/todoist-api-python
https://developer.todoist.com/rest/v2/?python#updating-a-task
"""

from todoist_api_python.api_async import TodoistAPIAsync
from conf.settings import TDIST_API_TOKEN

CLIENT = TodoistAPIAsync(TDIST_API_TOKEN)


def get_priority(content: str) -> int | None:
    for priority in range(1, 5):
        if f"p{priority}" in content:
            return priority
    return None


async def add_task(content: str):
    priority = get_priority(content)
    content = content.replace(f"p{priority}", "")
    content = content.strip()
    await CLIENT.add_task(content=content, labels=["from_watson"], priority=priority)
