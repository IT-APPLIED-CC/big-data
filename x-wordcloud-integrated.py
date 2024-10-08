import tweepy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Authentication for API v1.1 (OAuth1.0)
API_KEY = 'U6wuxgLvs4lFJdrwt3k37e1KE'
API_SECRET_KEY = 'K3tRDmQml8ekbALmw53VZ7V0WjijqO8FneMS7TOMP4IyblFhOJ'
ACCESS_TOKEN = '1249555754727534597-8VC5F3fZ61W29wv49wOPPJ935QHKoN'
ACCESS_TOKEN_SECRET = 'xRnvoagO0yvJoMgrwxcDlWl5K5KfRC1ph3jjFk7tCvoLt'

# Authentication for API v1.1
auth_v1 = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth_v1)

# Step 2: Authentication for API v2 (Bearer Token)
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGUZwQEAAAAASmoYz593nwFsgft4Rpt8jo9NNog%3Dt25Mk7G6zlqLrZNYivwBg75HHkrsa0sJCauzzud8oC1cozE4Rd'

# Authentication for API v2
client_v2 = tweepy.Client(bearer_token=BEARER_TOKEN)

# Step 3: Fetch tweets using API v1.1 (user timeline)
def fetch_tweets_v1(username, tweet_count):
    try:
        tweets = api_v1.user_timeline(screen_name=username, count=tweet_count, tweet_mode='extended')
        tweet_text = ''
        for tweet in tweets:
            tweet_text += tweet.full_text + ' '
        return tweet_text
    except tweepy.TweepyException as e:
        print(f"An error occurred: {e}")
        return ''

# Step 4: Fetch tweets using API v2 (search recent tweets)
def fetch_tweets_v2(query, tweet_count):
    try:
        response = client_v2.search_recent_tweets(query=query, max_results=tweet_count, tweet_fields=['text'])
        if response.data:
            tweet_text = ''
            for tweet in response.data:
                tweet_text += tweet['text'] + ' '
            return tweet_text
        else:
            print("No tweets found for the given query.")
            return ''
    except tweepy.TweepyException as e:
        print(f"An error occurred: {e}")
        return ''

# Step 5: Generate word cloud
def create_wordcloud(text):
    if text:
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    else:
        print("No text to generate a word cloud.")

# Step 6: Main Program
if __name__ == "__main__":
    print("Choose the API to use for fetching tweets:")
    print("1. Fetch tweets from a user's timeline (API v1.1)")
    print("2. Fetch recent tweets based on a search query (API v2)")
    
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        # API v1.1 (User Timeline)
        user = input("Enter the Twitter username: ")  # e.g., 'TwitterUsername'
        tweet_count = int(input("Enter the number of tweets to fetch: "))
        tweets_text = fetch_tweets_v1(user, tweet_count)
    elif choice == '2':
        # API v2 (Search Recent Tweets)
        query = input("Enter the search query: ")  # e.g., 'Python programming'
        tweet_count = int(input("Enter the number of tweets to fetch (max 100): "))
        tweets_text = fetch_tweets_v2(query, tweet_count)
    else:
        print("Invalid choice!")
        exit()

    # Create word cloud from the fetched tweets
    create_wordcloud(tweets_text)
