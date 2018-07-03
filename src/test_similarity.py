import csv
import pickle

import pandas as pd

from group_labels import child, common


def find_tweets(user, topics):
    tweets = []
    tweet_ids = []
    with open(f'../data/labels/{user}') as labels_file:
        for label_line in labels_file.readlines():
            items = label_line.split(',')
            if items[1] in topics:
                tweet_ids.append(items[0])

        df = pd.read_csv(f'../data/tweets/{user.replace("label2v", "tweets")}', header=0, encoding="utf-8")
        for _, row in df.iterrows():
            if str(row['tweet_id']) in tweet_ids:
                tweets.append(row['text'])
    return tweets


def print_result(sorted_pairs, users, results_num):
    for similar_pair, similarity in sorted_pairs[:results_num]:
        common_groups = common(users[similar_pair[0]], users[similar_pair[1]])
        common_topics = []
        for group in common_groups:
            common_topics.extend(child(group, users[similar_pair[0]]))
            common_topics.extend(child(group, users[similar_pair[1]]))
        common_topics = set(common_topics)
        tweets = set((find_tweets(similar_pair[0], common_topics) + find_tweets(similar_pair[1], common_topics))[:10])
        tweets = '\n'.join(tweets)
        common_topics = ', '.join(set(common_topics))
        print(f'Users: {similar_pair}\nDistance: {similarity}')
        print(f'Common groups: {common_groups}')
        print(f'Common topics: {common_topics}')
        print(f'Common tweets:\n{tweets}')


if __name__ == '__main__':
    with open('../saves/result_users.txt', 'rb') as input:
        users = pickle.load(input)
    with open('../saves/result_users_matrix.txt', 'rb') as fh:
        users_matrix = pickle.load(fh)
    with open('../saves/result_kmeans.txt', 'rb') as fh:
        kmeans = pickle.load(fh)
    with open('../saves/result_dataset.txt', 'rb') as fh:
        dataset = pickle.load(fh)
    with open('../saves/result_labels_vec_list.txt', 'rb') as fh:
        labels_vec_list = pickle.load(fh)

    # print 5 most similar users
    print('Most different users:')
    print_result(sorted(users_matrix.items(), key=lambda x: x[1]), users, 5)
    # print 5 most distant users
    print('Most similar users:')
    print_result(sorted(users_matrix.items(), key=lambda x: x[1], reverse=True), users, 5)



