import tweepy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Authenticate to Twitter
API_KEY = 'U6wuxgLvs4lFJdrwt3k37e1KE'
API_SECRET_KEY = 'K3tRDmQml8ekbALmw53VZ7V0WjijqO8FneMS7TOMP4IyblFhOJ'
ACCESS_TOKEN = '1249555754727534597-8VC5F3fZ61W29wv49wOPPJ935QHKoN'
ACCESS_TOKEN_SECRET = 'xRnvoagO0yvJoMgrwxcDlWl5K5KfRC1ph3jjFk7tCvoLt'

# Twitter authentication
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Step 2: Fetch tweets
def fetch_tweets(username, tweet_count):
    tweets = api.user_timeline(screen_name=username, count=tweet_count, tweet_mode='extended')
    tweet_text = ''
    for tweet in tweets:
        tweet_text += tweet.full_text + ' '
    return tweet_text

# Step 3: Generate word cloud
def create_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Step 4: Main Program
if __name__ == "__main__":
    user = 'TwitterUsername'  # Replace with the target Twitter username
    tweet_count = 100         # Number of tweets to fetch
    tweets_text = fetch_tweets(user, tweet_count)
    create_wordcloud(tweets_text)
