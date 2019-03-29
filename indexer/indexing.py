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
        "No. likes":    {"type":"integer"} 
      }
    }
  }
}'''


def create_index(name="tweet_index", es_host="searchly", filepath="data/data.json"):
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


def query(name="tweet_index", match_word="MAGA", sort_by="recent", es_host="searchly"):
    """
    name: name of the index
    match_word: keyword to be matched
    sort_by:recent/relevant
    """
    # print(es.search(index=name, body={"query": {"match": {'Content':match_word}}}))
    if es_host == "searchly":
        es = es_searchly
    elif es_host == "bonsai":
        es = es_bonsai
    else:
        raise RuntimeError("Unknown elastic host", es_host)

    if sort_by == "recent":
        return es.search(
            index=name,
            body={
                "query": {
                    "match": {
                        "Content": match_word
                    }
                },
                "sort": [
                    {"Timestamp": {"order": "desc"}}
                ]
            }
        )
    elif sort_by == "relevant":
        return es.search(
            index=name,
            body={
                "query": {
                    "match": {
                        "Content": match_word
                    }
                },
                "sort": [
                    {
                        "No. likes": {"order": "desc"},
                        "No. retweets": {"order": "desc"},
                    }
                ]
            }
        )
