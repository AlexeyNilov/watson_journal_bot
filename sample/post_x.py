from tweepy.asynchronous import AsyncClient
from tweepy.errors import TweepyException
import asyncio
from conf.settings import X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET

# Initialize the Async Client
client = AsyncClient(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET,
)


async def post_tweet(text):
    """Asynchronously posts a tweet using Tweepy."""
    try:
        response = await client.create_tweet(text=text)
        print(f"Tweet posted successfully! ID: {response.data['id']}")
    except TweepyException as e:
        print(f"Failed to post tweet: {e}")


# Run the async function
if __name__ == "__main__":
    asyncio.run(post_tweet("Hello, world! This is an async Tweepy tweet 🚀"))
