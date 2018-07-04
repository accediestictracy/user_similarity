import os
import re
import shutil

import csv
import enchant
import pandas as pd
import RAKE

# from sentiment_score.sentiment import sentiment_score


DATA_DIR = '../data'


def filter(tweet, dictionary):
    print(tweet)
    if tweet.startswith('RT @'):
        tweet = tweet[tweet.index(' ', 3) + 1:]
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'[^ \n\ra-zA-Z]', '', tweet, flags=re.MULTILINE)
    english_words = []
    for word in tweet.split():
        if word.startswith('@'):
            continue
        word = re.sub(r'(\w)\1+', r'\1', word)
        if dictionary.check(word) or word in ['Trump', ] and word not in ['RT', 'rt', 'Rt']:
            english_words.append(word.lower())
    print(english_words)
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
    label2vec = word2vec(os.path.join(DATA_DIR, 'glove_twitter_27B_25d.txt'))

    for file in sorted(os.listdir(directory)):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(directory, file), header=0, encoding="utf-8")
            new_df = pd.DataFrame(columns=['tweet_id', 'screen_name', 'created_at', 'hashtags', 'text'])
            new_df.set_index(['tweet_id'])
            vectorlist = []
            for _, row in df.iterrows():
                filtered = filter(row['text'], dictionary)
                if len(filtered) and all(len(x) > 3 for x in filtered):
                    row['text'] = ' '.join(filtered)
                    new_df = new_df.append(row)
                    labels = rake.run(' '.join(filtered))
                    if len(labels):
                        for keyword in labels[0][0].split():
                            try:
                                vector = label2vec[keyword]
                                print(filtered)
                                print(labels)
                                print(keyword)
                                to_add_vector = [row['tweet_id']] + vector
                                vectorlist.append(to_add_vector)
                                break
                            except KeyError:
                                pass
            new_df.to_csv(os.path.join(DATA_DIR, 'preprocessed', file.replace('tweets', 'prepped')))
            with open(os.path.join(DATA_DIR, 'labels', file.replace("tweets", "label2v")), 'w') as f:
                writer = csv.writer(f)
                writer.writerows(vectorlist)


if __name__ == '__main__':
    for dirname in ['labels', 'preprocessed']:
        if os.path.isdir(os.path.join(DATA_DIR, dirname)):
            shutil.rmtree(os.path.join(DATA_DIR, dirname))
        os.makedirs(os.path.join(DATA_DIR, dirname))

    process_tweets(os.path.join(DATA_DIR, 'tweets'))
