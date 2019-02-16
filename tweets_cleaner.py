import csv

from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

FILE_NAME = "04-Feb-2019.csv"
CONTENT_COLUMN = 4

if __name__ == '__main__':
    text_processor = TextPreProcessor(
        # terms that will be ignored
        # possible values: ['email', 'percent', 'money', 'phone', 'user', 'time', 'url', 'date', 'hashtag']
        omit = [],

        # terms that will be normalized
        # possible values: ['email', 'percent', 'money', 'phone', 'user', 'time', 'url', 'date', 'hashtag']
        normalize=['url', 'email', 'percent', 'money', 'phone', 'user', 'time', 'date', 'number'],

        # terms that will be annotated
        # possible values: ['hashtag', 'allcaps', 'elongated', 'repeated', 'emphasis', 'censored']
        annotate=["hashtag", "allcaps", "elongated", "repeated", 'emphasis', 'censored'],
        all_caps_tag='wrap',

        fix_text=True,  # fix bad unicode and HTML tokens  
        unpack_hashtags=True,  # perform word segmentation on hashtags
        unpack_contractions=False,  # Unpack contractions (can't -> can not)
        
        # select a tokenizer. You can use SocialTokenizer, or pass your own
        # the tokenizer, should take as input a string and return a list of tokens
        tokenizer=SocialTokenizer(lowercase=False).tokenize,
        
        # corpus from which the word statistics are going to be used 
        # for word segmentation 
        segmenter="twitter", 
        
        # corpus from which the word statistics are going to be used 
        # for spell correction
        corrector="twitter",
        spell_correction=True,
        spell_correct_elong=False,  # spell correction for elongated words

        # list of dictionaries, for replacing tokens extracted from the text,
        # with other expressions. You can pass more than one dictionaries.
        dicts=[emoticons]
    )

    with open("data/" + FILE_NAME, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        with open("data/" + FILE_NAME.split(".")[0] + "_normalized.csv", 'w', newline='', encoding='utf-8') as w:
            writer = csv.writer(w)
            header = next(reader)
            header.insert(CONTENT_COLUMN + 1, "Normalized")
            writer.writerow(header)
            print("Processing tweets...")
            for row in reader:
                content = row[CONTENT_COLUMN]
                row.insert(CONTENT_COLUMN + 1, " ".join(text_processor.pre_process_doc(content)))
                writer.writerow(row)
