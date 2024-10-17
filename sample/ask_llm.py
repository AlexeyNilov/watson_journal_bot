import asyncio
from service.llm import generate_text

prompt = "Idea for a new blog post"
context = """You are a highly successful blogger."""
asyncio.run(generate_text(context=context, prompt=prompt))
