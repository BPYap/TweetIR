DATA_DIR = "../data/"
CSV_NAME = "04-Feb-2019"
FIELDS = ["Username", "Full name", "URL", "Timestamp", "Content", "No. replies", "No. retweets", "No. likes"]
JACCARD_THRESHOLD = 0.8

if __name__ == '__main__':
    import csv

    import spacy
    from tqdm import tqdm

    print("Initializing spacy...")
    nlp = spacy.load('en_core_web_sm')

    def contain_similar(tokens_set, list_of_tokens_sets):
        for t in list_of_tokens_sets:
            num_intersects = len(tokens_set.intersection(t))
            num_unions = len(tokens_set.union(t))
            jaccard_coefficient = num_intersects / num_unions
            if jaccard_coefficient >= JACCARD_THRESHOLD:
                return True

        return False

    print("Calculating file size...")
    total = -1
    with open(DATA_DIR + CSV_NAME + '.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for _ in reader:
            total += 1

    with open(DATA_DIR + CSV_NAME + '.csv', 'r', encoding='utf-8', newline='') as f:
        print("Processing file...")
        reader = csv.DictReader(f, FIELDS)
        rows = []
        list_of_tokens = []
        for row in tqdm(reader, total=total):
            tokens = set([token.text.lower() for token in nlp(row["Content"])])
            if not contain_similar(tokens, list_of_tokens):
                rows.append(row)
                list_of_tokens.append(tokens)
        print("Done. Removed {} similar tweets".format(total - len(rows)))

        print("Writing to file...")
        filepath = DATA_DIR + CSV_NAME + "_similar_removed.csv"
        with open(filepath, 'a', encoding='utf-8', newline='') as w:
            writer = csv.DictWriter(w, FIELDS)
            for row in tqdm(rows):
                writer.writerow(row)
        print("Done. Reduced tweets are written to", filepath)
