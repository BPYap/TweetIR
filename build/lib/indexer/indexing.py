import json
import re

from elasticsearch import Elasticsearch


with open("../config.json", 'r') as f:
    urls = json.load(f)
    es_searchly = Elasticsearch([urls["searchly"]])

    bonsai_url = urls["bonsai"]
    auth = re.search('https://(.*)@', bonsai_url).group(1).split(':')
    host = bonsai_url.replace('https://%s:%s@' % (auth[0], auth[1]), '')
    es_header = [{
        'host': host,
        'port': 443,
        'use_ssl': True,
        'http_auth': (auth[0], auth[1])
    }]
    es_bonsai = Elasticsearch(es_header)

mapping = '''{
  "mappings": {
    "tweet": { 
      "properties": { 
        "Username":     {"type": "text"}, 
        "Full name":    {"type": "text"},
        "URL":          {"type": "text" },
        "Timestamp":    {"type":"date", "format": "yyyy-MM-dd HH:mm:ss"},
        "Content":      {"type":"text"},
        "No. replies":  {"type":"integer"},
        "No. retweets": {"type":"integer"}, 
        "No. likes":    {"type":"integer"},
        "Sentiment":    {"type":"integer"}
      }
    }
  }
}'''


class Tweet:
    def __init__(self, json_string):
        self.username = json_string['Username']
        self.fullname = json_string['Full name']
        self.url = json_string['URL']
        self.timestamp = json_string['Timestamp']
        self.content = json_string['Content']
        self.num_reply = json_string['No. replies']
        self.num_retweet = json_string['No. retweets']
        self.num_like = json_string['No. likes']
        self.sentiment = json_string['Sentiment']


def create_index(name="tweet_index", es_host="searchly", filepath="../data/data.json"):
    if es_host == "searchly":
        es = es_searchly
    elif es_host == "bonsai":
        es = es_bonsai
    else:
        raise RuntimeError("Unknown elastic host", es_host)

    if es.indices.exists(name):
        es.indices.delete(name)
    es.indices.create(index=name, body=mapping)
    with open(filepath) as f:
        data = json.load(f)
    for i, record in enumerate(data):
        es.index(index=name, doc_type='tweet', id=i, body=record)


def add_index(tweets, name="tweet_index", es_host="searchly"):
    if es_host == "searchly":
        es = es_searchly
    elif es_host == "bonsai":
        es = es_bonsai
    else:
        raise RuntimeError("Unknown elastic host", es_host)

    # fetch the last index
    _id = es.count(index=name)["count"]

    for record in json.loads(tweets):
        mapped_record = dict()
        mapped_record["Username"] = record["username"]
        mapped_record["Full name"] = record["full_name"]
        mapped_record["URL"] = record["url"]
        mapped_record["Timestamp"] = record["timestamp"].replace("T", " ")
        mapped_record["Content"] = record["content"]
        mapped_record["No. replies"] = record["num_reply"]
        mapped_record["No. retweets"] = record["num_retweet"]
        mapped_record["No. likes"] = record["num_like"]
        mapped_record["Sentiment"] = record["sentiment"]
        es.index(index=name, doc_type='tweet', id=_id, body=mapped_record)
        _id += 1

    es.indices.refresh([name])


def query(name="tweet_index", match_word="MAGA", sort_by="recent", filter_by=None,
          es_host="searchly", search_after=None):
    """
    name: name of the index
    match_word: keyword to be matched
    sort_by: recent/relevant
    """
    # print(es.search(index=name, body={"query": {"match": {'Content':match_word}}}))
    if es_host == "searchly":
        es = es_searchly
    elif es_host == "bonsai":
        es = es_bonsai
    else:
        raise RuntimeError("Unknown elasticsearch host", es_host)

    body = {
        "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"Content": match_word}}
                    ]
                }
        },
        'suggest':
            {
                'text': match_word,
                'suggestions': {
                    "phrase": {
                        "field": "Content",
                        "size": 1,
                        "gram_size": 3,
                        "max_errors": 2,
                        "direct_generator": [{
                            "field": "Content",
                            "suggest_mode": "always"
                        }],
                    }
                }
            }
    }
    if search_after:
        body["search_after"] = search_after

    if sort_by == "recent":
        body["sort"] = [{"Timestamp": {"order": "desc"}}, {"_id": "asc"}]
    else:
        body['sort'] = [{"No. likes": {"order": "desc"}, "No. retweets": {"order": "desc"}}, {"_id": "asc"}]

    if filter_by is not None:
        body["query"]["bool"]["filter"] = [{"term": {"Sentiment": filter_by}}]

    json_result = es.search(index=name, body=body, size=50)
    suggestions = json_result["suggest"]["suggestions"][0]["options"]
    if json_result['hits']['total'] == 0 and suggestions:
        corrected = suggestions[0]
        response = query(match_word=corrected["text"], sort_by=sort_by)
        response["corrected"] = corrected["text"]
        return response

    results = []
    search_after = None

    for tweet in json_result['hits']['hits']:
        results.append(Tweet(tweet['_source']))
        search_after = tweet['sort']

    response = {
        "time_taken": json_result['took'] / 1000,
        "total_result": json_result['hits']['total'],
        "results": results,
        "search_after": search_after
    }

    return response
