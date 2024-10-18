from openai import AsyncOpenAI
from conf.settings import OPENAI_API_KEY
from functools import lru_cache


@lru_cache(maxsize=None)  # Cache all results without limit
def read_file(file_path: str) -> str:
    """Reads the content of a text file and returns it as a string."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


OPENAI_CLIENT = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_text(prompt: str, context: str, model: str = "gpt-4o-mini") -> str:
    response = await OPENAI_CLIENT.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ],
        temperature=1,
    )

    return response.choices[0].message.content.strip()


BLOGGER = read_file("prompts/blogger.md")
ASSISTANT = read_file("prompts/assistant.md")
SUMMARIZER = read_file("prompts/summarizer.md")


async def get_tweet_from_llm(prompt: str):
    return await generate_text(prompt=prompt, context=BLOGGER)


async def get_retrospection_from_llm(prompt: str):
    return await generate_text(prompt=prompt, context=ASSISTANT, model="gpt-4o")


async def get_summary_from_llm(prompt: str):
    return await generate_text(prompt=prompt, context=SUMMARIZER)
