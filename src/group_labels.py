from collections import defaultdict
import json
import os
import pickle
import shutil

import numpy as np
from scipy import spatial
from sklearn.cluster import KMeans


def common(usera, userb):
    avga = np.average([len(x) for x in usera['groups'].values()])
    avgb = np.average([len(x) for x in userb['groups'].values()])
    ratio = 1
    s1 = set([key for key, value in usera['groups'].items() if len(value) > avga * ratio])
    return s1.intersection(set([key for key, value in userb['groups'].items() if len(value) > avgb * ratio]))


def child(label, user):
    return user['groups'][label]


def calculate_similarity_matrix():
    dataset = []
    labels_vec_list = []
    users = defaultdict(dict)
    j = 0
    for file in os.listdir("../data/labels"):
        usrtopic2vecs = defaultdict(list)
        usrtopicscores = defaultdict(list)
        if not os.path.isfile(f"../data/scores/{file.replace('label2v', 'tweets-1')}"):
            continue
        with \
                open(f"../data/labels/{file}") as labels_file_handler, \
                open(f"../data/scores/{file.replace('label2v', 'tweets-1')}") as scores_file_handler:
            score_lines = scores_file_handler.readlines()
            labels_lines = labels_file_handler.readlines()
            if len(score_lines) == 0 or len(labels_lines) == 0:
                continue
            for line in labels_lines:
                label_items = line.strip().split(',')
                score = None
                for line2 in score_lines:
                    score_items = line2.split(',')
                    if score_items[0] == label_items[0]:
                        score = score_items[-1]
                if not score:
                    continue

                vector = [float(f) for f in label_items[2:]]
                dataset.append(vector)
                usrtopic2vecs[label_items[1]].append(vector)
                usrtopicscores[label_items[1]].append(float(score))
                labels_vec_list.append([file, label_items[1]])
        if not len(usrtopic2vecs) or not len(usrtopicscores):
            continue
        users[file]['data'] = usrtopic2vecs
        users[file]['topicscores'] = usrtopicscores

        #j += 1
        if j == 20:
            break

    clusters = 500
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(dataset)
    labels = kmeans.labels_

    for i, datarow in enumerate(dataset):
        topic = labels_vec_list[i][1]
        user = labels_vec_list[i][0]
        users[user].setdefault('groups', {}).setdefault(labels[i], []).append(topic)

    max_clist = 0
    users_matrix = {}
    counter = 0
    for user1, uservalue1 in users.items():
        for user2, uservalue2 in users.items():
            pair = tuple(sorted((user1.lower(), user2.lower())))
            if user1 == user2 or pair in users_matrix:
                continue
            clist = common(uservalue1, uservalue2)  # common groups of user i and user j
            num = len(clist)
            max_clist = max(max_clist, num)
            user1_child = []
            user2_child = []
            vec_user1 = 0
            vec_user2 = 0
            for k in clist:
                user1_child.extend(child(k, uservalue1))  # labels of user_i in group[k]
                user2_child.extend(child(k, uservalue2))

                for tag in user1_child:
                    vec_user1 += np.array(uservalue1['data'][tag][0]) * np.average(uservalue1['topicscores'][tag])
                vec_user1 /= len(user1_child)
                for tag in user2_child:
                    vec_user2 += np.array(uservalue2['data'][tag][0]) * np.average(uservalue2['topicscores'][tag])
                vec_user2 /= len(user2_child)

            if clist:
                users_matrix[pair] = (1-spatial.distance.cosine(vec_user1, vec_user2)) * num / 1000.0
            else:
                users_matrix[pair] = 0

            counter += 1
            print(counter)

    if os.path.isdir('../saves'):
        shutil.rmtree('../saves')
    os.makedirs('../saves')
    with open('../saves/result_users.txt', 'wb') as fh:
        pickle.dump(users, fh, pickle.HIGHEST_PROTOCOL)
    with open('../saves/result_users_matrix.txt', 'wb') as fh:
        pickle.dump(users_matrix, fh, pickle.HIGHEST_PROTOCOL)
    with open('../saves/result_kmeans.txt', 'wb') as fh:
        pickle.dump(kmeans, fh, pickle.HIGHEST_PROTOCOL)
    with open('../saves/result_dataset.txt', 'wb') as fh:
        pickle.dump(dataset, fh, pickle.HIGHEST_PROTOCOL)
    with open('../saves/result_labels_vec_list.txt', 'wb') as fh:
        pickle.dump(labels_vec_list, fh, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    calculate_similarity_matrix()
