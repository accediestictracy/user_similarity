"""
Sentiment prediction module
"""
import os
import shutil

import nltk
import numpy as np
import pandas as pd

from cPickle import load

def get_word_index_array(words, word2index):
    u"""
    Transform the words into list of int(word index)
    
    Note: Unknown words are dropped
    
    >>> words = [u"I", u"love", u"you", u"RANDOM STUFF"]
    >>> word2index = {u"I": 0, u"love": 1, u"you": 2}
    >>> get_word_index_array(words, word2index)
    [0, 1, 2]
    """
    return [word2index[w] 
            for w in words 
            if word2index.get(w) is not None # filter out those unknown
    ]


def pad_sents(sents, padding_token_index):
    """

    Pad the sents(in word index form) into same length so they can form a matrix
    
    # 15447
    >>> sents = [[1,2,3], [1,2], [1,2,3,4,5]]
    >>> pad_sents(sents, padding_token_index = -1)
    [[1, 2, 3, -1, -1], [1, 2, -1, -1, -1], [1, 2, 3, 4, 5]]
    """
    max_len_sent = max(sents, 
                       key = lambda sent: len(sent))
    max_len = len(max_len_sent)
    
    get_padding = lambda sent: [padding_token_index] * (max_len - len(sent))
    padded_sents = [(sent + get_padding(sent))
                    for sent in sents]
    return padded_sents


WORD2INDEX = load(open("data/twitter.pkl"))[3]
PADDING_INDEX = WORD2INDEX[u"<PADDING>"]

from param_util import load_dcnn_model_params
from dcnn import DCNN

params = load_dcnn_model_params("models/filter_widths=8,6,,batch_size=10,,ks=20,8,,fold=1,1,,conv_layer_n=2,,ebd_dm=48,,l2_regs=1e-06,1e-06,1e-06,0.0001,,dr=0.5,0.5,,nkerns=7,12.pkl")

MODEL = DCNN(params)

def sentiment_scores_of_sents(sents):
    """
    Predict the sentiment positive scores for a bunch of sentences
    
    >>> sentiment_scores_of_sents([u'simultaneously heart breaking and very funny , the last kiss is really all about performances .', u'( u ) stupid .'])
    array([ 0.78528505,  0.0455901 ])
    """
    word_indices = [get_word_index_array(nltk.word_tokenize(sent), WORD2INDEX)
                    for sent in sents]

    x = np.asarray(
        pad_sents(word_indices, PADDING_INDEX), 
        dtype = np.int32
    )

    scores = MODEL._p_y_given_x(x)

    return scores[:, 1] # return `positiveness`


def sentiment_score(sent):
    """simple wrapper around the more general case"""
    return sentiment_scores_of_sents([sent])[0]


def get_sentiment_scores():
    if os.path.isdir('../../data/scores'):
        shutil.rmtree('../../data/scores')
    os.makedirs('../../data/scores/')
    files = os.listdir('../../data/tweets')
    for file in sorted(files):
        if file.endswith(".csv"):
            print(file)
            df = pd.read_csv('../../data/tweets/' + file, header=0, encoding="utf-8")
            with open('../../data/scores/' + file.replace('tweets', 'tweets-1'), 'w') as file_handler:
                for index, row in df.iterrows():
                    print(row)
                    vector = [
                        str(row['tweet_id']),
                        str(row.get('screen_name', '')).encode('utf-8'),
                        row['created_at'].encode('utf-8'),
                        row.get('hashtags', '').encode('utf-8'),
                        str(sentiment_score(row['text']))
                    ]
                    file_handler.write(','.join(vector) + '\n')


if __name__ == '__main__':
    get_sentiment_scores()
