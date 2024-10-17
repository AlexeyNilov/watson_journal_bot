import requests
from conf.settings import X_TOKEN, X_USER_NAME


def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {X_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data["data"]["id"]
        print(f"User ID for @{username}: {user_id}")
        return user_id
    else:
        print(f"Failed to fetch user ID: {response.status_code}")
        print(response.json())
        return None


ACCOUNT_ID = get_user_id(X_USER_NAME)
print(ACCOUNT_ID)
exit()


# def create_headers(bearer_token):
#     return {
#         "Authorization": f"Bearer {bearer_token}",
#         "Content-Type": "application/json"
#     }

# def post_tweet(text):
#     url = "https://api.twitter.com/2/tweets"
#     headers = create_headers(BEARER_TOKEN)

#     payload = {
#         "text": text  # Tweet content
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code == 201:
#         print("Tweet posted successfully!")
#         print(f"Response: {response.json()}")
#     else:
#         print(f"Failed to post tweet: {response.status_code}")
#         print(response.json())

# # Example usage
# post_tweet("Hello, world! This is a tweet posted using Twitter API v2 🎉")
