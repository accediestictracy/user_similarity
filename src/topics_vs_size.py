import os
import re

import enchant
import matplotlib.pyplot as plt
import pandas as pd
import RAKE


def filter(tweet, dictionary):
    #print(tweet)
    if tweet.startswith('RT @'):
        tweet = tweet[tweet.index(' ', 3) + 1:]
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', ' ', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'[^ \n\ra-zA-Z]', ' ', tweet, flags=re.MULTILINE)
    english_words = []
    for word in tweet.split():
        if word.startswith('@'):
            continue
        for w in [word, re.sub(r'(\w)\1+', r'\1', word)]:
            if dictionary.check(w) or w in ['Trump', ] and w not in ['RT', 'rt', 'Rt']:
                english_words.append(w.lower())
                break
    #print(english_words)
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


def topics(sizes):
    dictionary = enchant.Dict("en_US")
    rake = RAKE.Rake('SmartStopList.py')
    label2vec = word2vec(os.path.join('../data-4', 'glove_twitter_27B_25d.txt'))
    result = {}
    all_keywords = set()

    all_set = os.listdir('../data/tweets')
    for set_index, file in enumerate(sorted(all_set)):
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join('../data/tweets', file), header=0, encoding="utf-8")
            except:
                continue

            for _, row in df.iterrows():
                filtered = filter(row['text'], dictionary)
                if len(filtered):
                    labels = rake.run(' '.join(filtered))
                    if len(labels):
                        for keyword in labels[0][0].split():
                            try:
                                # if len(keyword) < 3:
                                    # break
                                if keyword in label2vec:
                                    all_keywords.add(keyword)
                                    break
                            except KeyError:
                                pass
        print(f'{set_index} / {len(all_set)}')
        if set_index + 1 in sizes:
            result[set_index + 1] = len(all_keywords)
    return result


if __name__ == '__main__':
    data = topics([500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500])
    xs = sorted(data.keys())
    ys = [data[x] for x in xs]
    plt.plot(xs, ys, 'ro')
    plt.show()
    plt.savefig('topics_vs_size.png')
