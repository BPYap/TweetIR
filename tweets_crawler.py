import csv

from twitterscraper import query_tweets

QUERY = "Donald Trump OR Donald J. Trump"
LIMIT = 50000
LANG = "en"

if __name__ == '__main__':
    tweets = query_tweets(QUERY, limit=LIMIT, lang=LANG)
    
    with open("data/" + QUERY + ".csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Username", "Full name", "URL", "Timestamp", "Content", 
                "No. replies", "No. retweets", "No. likes"])
        seen_tweets = set()
        for tweet in tweets:
            if tweet.text not in seen_tweets:
                writer.writerow([tweet.user, tweet.fullname, tweet.url, tweet.timestamp, tweet.text, 
                        tweet.replies, tweet.retweets, tweet.likes])
                seen_tweets.add(tweet.text)
