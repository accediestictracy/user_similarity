import os
import re

import csv
import enchant
import pandas as pd
import RAKE


def filter(tweet, dictionary):
    print(tweet)
    if tweet.startswith('RT @'):
        tweet = tweet[tweet.index(' ', 3) + 1:]
        print(tweet)
    english_words = []
    regex = re.compile('[^a-zA-Z]')
    tweet = regex.sub(' ', tweet)
    for word in tweet.split():
        if dictionary.check(word) or word in ['Trump', ] and word not in ['RT', 'rt', 'Rt']:
            english_words.append(word)
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


def process_tweets():
    dictionary = enchant.Dict("en_US")
    rake = RAKE.Rake('SmartStopList.py')
    label2vec = word2vec('../data/glove_twitter_27B_25d.txt')
    for file in sorted(os.listdir("../data/tweets")):
        if file.endswith(".csv"):
            df = pd.read_csv(f'../data/tweets/{file}', header=0, encoding="utf-8")
            vectorlist = []
            for index, tweet in enumerate(df['text']):
                filtered = filter(tweet, dictionary)
                if len(filtered):
                    labels = rake.run(' '.join(filtered))
                    if len(labels):
                        vector = []
                        for keyword in labels[0][0].split():
                            try:
                                vector = label2vec[keyword]
                                print(tweet)
                                print(filtered)
                                print(labels)
                                print(keyword)
                                to_add_vector = [df['tweet_id'][index]] + vector
                                vectorlist.append(to_add_vector)
                                break
                            except KeyError:
                                pass

            with open(f'../data/labels/{file.replace("tweets", "label2v")}', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(vectorlist)


if __name__ == '__main__':
    process_tweets()