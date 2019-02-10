import csv
import string
from collections import Counter

import matplotlib.pyplot as plt
import spacy

nlp = spacy.load('en_core_web_sm')

FILE_NAME = "04-Feb-2019.csv"

if __name__ == '__main__':
    total_records = 0
    char_count = Counter()
    word_count = Counter()

    with open("data/" + FILE_NAME, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            content = row[4]
            total_records += 1
            char_count.update(content)
            doc = nlp(content)
            for token in doc:
                word_count.update([token.text])

    print("Number of records:", total_records)
    print("Number of characters:", sum(char_count.values()))
    print("Number of unique characters:", len(char_count))
    print("Number of words:", sum(word_count.values()))
    print("Number of unique words:", len(word_count))

    print("\nTop-30 most common words:")
    count = 0
    freqs = []
    words = []
    for word, count in word_count.most_common(100):
        if len(word) == 1 and word in string.punctuation:
            continue
        elif count == 30:
            break
        else:
            print("{:<10} count: {}".format(word, count))
            count += 1
            freqs.append(count)
            words.append(word)

    fig, ax = plt.subplots()
    plt.xticks(rotation=90)
    ax.plot(words, freqs)
    ax.set(xlabel='word', ylabel='frequency')
    ax.grid()
    fig.savefig("word_frequency.png")
    plt.show()
