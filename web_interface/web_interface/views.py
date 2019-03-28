from django.shortcuts import render

from indexer.indexing import query as elastic_query


def home(request):
    outputs = []
    if "text_input" in request.POST and request.POST["text_input"] != "":
        # Get inputs from front-end UI and pre-process the input if necessary
        query = request.POST["text_input"]
        outputs.append({query: [str(elastic_query(match_word=query))]})  # TODO: parse JSON to display in tabular form

    return render(request, "index.html", {'name': "Home", "outputs": outputs})


def corpus(request):
    return render(request, "corpus.html", {'name': "Documentation"})


def sentiment(request):
    return render(request, "sentiment.html", {'name': "Documentation"})
