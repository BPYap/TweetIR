import datetime

from twitterscraper import query_tweets

LIMIT = 500
LANG = "en"


class Tweet:
    def __init__(self, scraper_tweet_object):
        self.username = scraper_tweet_object.user
        self.fullname = scraper_tweet_object.fullname
        self.url = scraper_tweet_object.url
        self.timestamp = scraper_tweet_object.timestamp
        self.content = scraper_tweet_object.text
        self.num_reply = scraper_tweet_object.replies
        self.num_retweet = scraper_tweet_object.retweets
        self.num_like = scraper_tweet_object.likes


def crawl(query, start_date=None, end_date=None, limit=LIMIT):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    tweets = query_tweets(query, begindate=start_date, enddate=end_date, limit=limit, lang=LANG)

    results = set()
    for tweet in tweets:
        results.add(Tweet(tweet))
        if len(results) == limit:
            break

    return list(results)  # shuffle tweets
