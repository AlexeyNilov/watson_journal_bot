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

    resp = response.choices[0].message.content.strip()
    print(resp)
    return resp
