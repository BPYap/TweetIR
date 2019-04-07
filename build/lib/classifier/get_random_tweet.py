DATA_DIR = "../data/"
CSV_NAME = "04-Feb-2019_similar_removed"
FIELDS = ["Username", "Full name", "URL", "Timestamp", "Content", "No. replies", "No. retweets", "No. likes"]
COUNT = 1000

if __name__ == '__main__':
    import csv
    import random

    from tqdm import tqdm

    print("Writing to file...")
    with open(DATA_DIR + CSV_NAME + '.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, FIELDS)
        next(reader)
        filepath = "{}_random_{}.csv".format(DATA_DIR + CSV_NAME, COUNT)
        with open(filepath, 'a', encoding='utf-8', newline='') as w:
            writer = csv.writer(w)
            writer.writerow(["Row Number", "Content", "Label"])
            rows_written = 0
            for i, row in tqdm(enumerate(reader), total=COUNT):
                if random.random() >= 0.9:
                    writer.writerow([i, row["Content"]])
                    rows_written += 1
                    if rows_written == COUNT:
                        break
    print("Done. Selected tweets are written to", filepath)
