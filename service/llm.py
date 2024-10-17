from openai import AsyncOpenAI
from conf.settings import OPENAI_API_KEY


OPENAI_CLIENT = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_text(prompt: str, context: str) -> str:
    response = await OPENAI_CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()


BLOGGER_CONTEXT = """You are a highly successful blogger and creative writer with expertise in crafting engaging,
colorful, and concise content for X (formerly Twitter). Your goal is to transform ideas into short, vibrant,
and attention-grabbing posts that resonate with the audience. Expand the provided ideas with creativity, wit,
and emotional depth, ensuring the tone fits social media engagement. Keep the posts short, punchy, and easy to read."""


async def get_tweet_from_llm(prompt: str):
    return await generate_text(prompt=prompt, context=BLOGGER_CONTEXT)
