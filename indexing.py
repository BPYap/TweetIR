from elasticsearch import Elasticsearch
import json
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
mapping='''{
  "mappings": {
    "_doc": { 
      "properties": { 
        "Username":    { "type": "text"  }, 
        "Full name":     { "type": "text"  }, 
        "URL":      { "type": "text" },
        "Timetamp": {"type":"date","fielddata": true}
        "Content":  {"type":"text"}
        "No.replies":{"type":"integer"}
        "No.retweets":{"type":"integer"} 
        "No.likes":   {"type":"integer"} 
      }
    }
  }
}'''


def create_index(name="tweet_index",filepath="data/data.json"):
    if es.indices.exists(name):es.indices.delete(name)
    es.indices.create(index=name,ignore=400,body=mapping)
    with open('data/data.json') as f:
       data = json.load(f)
    for i,record in enumerate(data):
        es.index(index=name, doc_type='tweet', id=i, body=record)


def query(name="tweet_index",match_word="MAGA"):
    '''
    name: name of the index
    match_word: keyword to be matched
    sort_by:recent/relevant
    '''
    print(es.search(index=name, body={"query": {"match": {'Content':match_word}}}))
