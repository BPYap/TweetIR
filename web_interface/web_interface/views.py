from django.shortcuts import render


def home(request):
    return render(request, "index.html", {'name': "Home"})


def corpus(request):
    return render(request, "corpus.html", {'name': "Corpus"})
