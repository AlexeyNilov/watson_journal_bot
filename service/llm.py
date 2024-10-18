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
        temperature=1,
    )

    return response.choices[0].message.content.strip()


BLOGGER_CONTEXT = """You are a brilliant thinker and skilled technical writer, specializing in creating concise, vibrant,
and engaging content for Twitter. Your goal is to transform ideas into short, attention-grabbing posts
that resonate with software developers and LLM enthusiasts. Each post should be under 250 characters, punchy, easy to read,
and optimized for social media engagement. Infuse the content with creativity, emotional depth,
and thoughtful insights while ensuring it sparks curiosity and aligns with the audience's technical interests."""


async def get_tweet_from_llm(prompt: str):
    return await generate_text(prompt=prompt, context=BLOGGER_CONTEXT)


async def get_tweet_from_llm_mock(prompt: str):
    print(prompt)
    return f"Prompt: {prompt}"
