import asyncio
from service.llm import generate_text

prompt = "Codify new ideas! View them as an opportunity to create new application and improve coding skills"
context = """You are a highly successful blogger and creative writer with expertise in crafting engaging,
colorful, and concise content for X (formerly Twitter). Your goal is to transform ideas into short, vibrant,
and attention-grabbing posts that resonate with the audience. Expand the provided ideas with creativity, wit,
and emotional depth, ensuring the tone fits social media engagement. Keep the posts short, punchy, and easy to read."""
asyncio.run(generate_text(context=context, prompt=prompt))
