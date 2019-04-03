from django.http import JsonResponse
from django.shortcuts import render

from indexer.indexing import query as elastic_query


def home(request):
    time_taken = 0
    total_results = 0
    query = None
    tweets = []
    search_after = None
    corrected = None
    if "text_input" in request.POST and request.POST["text_input"] != "":
        # Get inputs from front-end UI and pre-process the input if necessary
        query = request.POST["text_input"]
        response = elastic_query(match_word=query)

        time_taken = response["time_taken"]
        total_results = response["total_result"]
        tweets = response["results"]
        search_after = response["search_after"]
        corrected = None if "corrected" not in response else response["corrected"]

    arguments = {
        'name': "Home",
        "time_taken": time_taken,
        "total_results": total_results,
        "query": query,
        "tweets": tweets,
        "search_after": search_after,
        "corrected": corrected
    }

    return render(request, "home.html", arguments)


def get_page(request):
    query = request.POST["query"]
    search_after = None if "search_after[]" not in request.POST else request.POST.getlist("search_after[]")

    if search_after is not None and type(search_after) != list:
        search_after = [search_after]
    sort_by = "recent" if "relevant" not in request.POST else 'relevant'
    response = elastic_query(match_word=query, sort_by=sort_by, search_after=search_after)

    serialized = []
    for tweet in response["results"]:
        temp = dict()
        temp["username"] = tweet.username
        temp["timestamp"] = tweet.timestamp
        temp["url"] = tweet.url
        temp["content"] = tweet.content
        temp["num_reply"] = tweet.num_reply
        temp["num_retweet"] = tweet.num_retweet
        temp["num_like"] = tweet.num_like
        serialized.append(temp)

    return JsonResponse({"tweets": serialized, "search_after": response["search_after"]})


def index(request):
    arguments = None
    return render(request, "index.html", arguments)


def corpus(request):
    return render(request, "corpus.html", {'name': "Documentation"})


def sentiment(request):
    return render(request, "sentiment.html", {'name': "Documentation"})
