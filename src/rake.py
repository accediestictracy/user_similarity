import os
import re

import csv
import enchant
import pandas as pd
import RAKE

# from sentiment_score.sentiment import sentiment_score


def filter(tweet, dictionary):
    print(tweet)
    if tweet.startswith('RT @'):
        tweet = tweet[tweet.index(' ', 3) + 1:]
    tweet = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'[^ a-zA-Z]', '', tweet, flags=re.MULTILINE)
    print(tweet)
    english_words = []
    for word in tweet.split():
        if word.startswith('@'):
            continue
        word = re.sub(r'(\w)\1+', r'\1', word)
        if dictionary.check(word) or word in ['Trump', ] and word not in ['RT', 'rt', 'Rt']:
            english_words.append(word.lower())
    return english_words


def word2vec(model):
    result = {}
    regex = re.compile('[^a-zA-Z]')
    with open(model) as file_handler:
        for line in file_handler.readlines():
            elements = line.split()
            elements[0] = regex.sub(' ', elements[0])
            result[elements[0]] = [elements[0]] + [float(element) for element in elements[1:]]
    return result


def process_tweets(directory):
    dictionary = enchant.Dict("en_US")
    rake = RAKE.Rake('SmartStopList.py')
    label2vec = word2vec('../data/glove_twitter_27B_25d.txt')
    if not os.path.isdir('../data/labels/'):
        os.makedirs('../data/labels/')
    if not os.path.isdir('../data/preprocessed/'):
        os.makedirs('../data/preprocessed/')
    for file in sorted(os.listdir(directory)):
        if file.endswith(".csv"):
            df = pd.read_csv(f'../data/tweets/{file}', header=0, encoding="utf-8")
            vectorlist = []
            with open(f'../data/preprocessed/{file}', 'w') as file_handler:
                for index, tweet in enumerate(df['text']):
                    filtered = filter(tweet, dictionary)
                    if len(filtered):
                        labels = rake.run(' '.join(filtered))
                        if len(labels):
                            for keyword in labels[0][0].split():
                                try:
                                    vector = label2vec[keyword]
                                    print(filtered)
                                    print(labels)
                                    print(keyword)
                                    to_add_vector = [df['tweet_id'][index]] + vector
                                    vectorlist.append(to_add_vector)
                                    break
                                except KeyError:
                                    pass
                    file_handler.write(' '.join(filtered))

                with open(f'../data/labels/{file.replace("tweets", "label2v")}', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(vectorlist)


if __name__ == '__main__':
    process_tweets('../data/tweets')
