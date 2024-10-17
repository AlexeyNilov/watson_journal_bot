from tweepy.asynchronous import AsyncClient
from conf.settings import X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET


# Initialize the Async Client
X_CLIENT = AsyncClient(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_TOKEN_SECRET,
)


async def post_tweet(text):
    """Asynchronously posts a tweet using Tweepy."""
    await X_CLIENT.create_tweet(text=text)
