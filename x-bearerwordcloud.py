import tweepy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Twitter API v2 Authentication
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGUZwQEAAAAASmoYz593nwFsgft4Rpt8jo9NNog%3Dt25Mk7G6zlqLrZNYivwBg75HHkrsa0sJCauzzud8oC1cozE4Rd'  # Replace with your actual bearer token

# Twitter authentication using API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Step 2: Fetch tweets using API v2
def fetch_tweets_v2(query, tweet_count):
    try:
        response = client.search_recent_tweets(query=query, max_results=tweet_count, tweet_fields=['text'])
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

# Step 3: Generate word cloud
def create_wordcloud(text):
    if text:
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    else:
        print("No text to generate a word cloud.")

# Step 4: Main Program
if __name__ == "__main__":
    query = 'Python programming'  # Adjust the search term to what you're interested in
    tweet_count = 10              # Number of tweets to fetch (v2 limits max_results to 100)
    tweets_text = fetch_tweets_v2(query, tweet_count)
    create_wordcloud(tweets_text)
