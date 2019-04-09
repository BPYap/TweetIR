import csv

from indexing import create_index, query

QUERY = "trump"

create_index()
search_after_id = None
file = None
writer = None
while True:
    response = query(match_word=QUERY, search_after=search_after_id)
    if file is None:
        total_results = response["total_result"]
        time_taken = response["time_taken"]
        file = open("query={},total_result={},time_taken={}s.csv".format(QUERY, total_results, time_taken),
                    'a', encoding='utf-8', newline="")
        writer = csv.writer(file)
        writer.writerow(["Fullname", "URL", "Timestamp", "Content", "Replies", "Retweets", "Likes", "Sentiment"])

    tweets = response['results']
    if len(tweets) == 0:
        break
    else:
        for tweet in tweets:
            writer.writerow([tweet.fullname, tweet.url, tweet.timestamp, tweet.content,
                             tweet.num_reply, tweet.num_retweet, tweet.num_like, tweet.sentiment])

    search_after_id = response['search_after']

file.close()
