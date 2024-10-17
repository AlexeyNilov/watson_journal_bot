import tweepy
import asyncio

# Replace with your Twitter App's credentials
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

# Initialize the Async Client
client = tweepy.AsyncClient(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)


async def post_tweet(text):
    """Asynchronously posts a tweet using Tweepy."""
    try:
        response = await client.create_tweet(text=text)
        print(f"Tweet posted successfully! ID: {response.data['id']}")
    except tweepy.TweepyException as e:
        print(f"Failed to post tweet: {e}")


# Run the async function
if __name__ == "__main__":
    asyncio.run(post_tweet("Hello, world! This is an async Tweepy tweet 🚀"))
