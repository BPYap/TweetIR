import csv

from sentiment_classifier import inference

CSV_PATH = "../data/04-Feb-2019.csv"
OUTPUT_PATH = "../data/04-Feb-2019_with_sentiment.csv"

fieldnames = ["Username", "Full name", "URL", "Timestamp", "Content",
              "No. replies", "No. retweets", "No. likes"]
csvfile = open(CSV_PATH, 'r', encoding='utf-8', newline='')
reader = csv.DictReader(csvfile, fieldnames)
with open(OUTPUT_PATH, 'a', encoding='utf-8', newline='') as w:
    writer = csv.DictWriter(w, fieldnames + ["Sentiment"])
    writer.writeheader()
    for index, row in enumerate(reader):
        if index == 0:
            continue

        label = inference(row["Content"])
        row["Sentiment"] = label
        writer.writerow(row)
