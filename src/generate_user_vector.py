# -*- coding:utf-8 -*-

import os
import pandas as pd
import numpy as np


lst = os.listdir("user_timeline_score")

tags = []
users = []

for file in lst:
    if file.endswith(".csv"):
        df = pd.read_csv("user_timeline_score/"+file, header=0, encoding="utf-8")
        for i in df['hashtags']:
            tmp = i[1:-1]
            if tmp != "":
                tmp_tags = tmp.split("*")
                for t in tmp_tags:
                    if t not in tags:
                        tags.append(t)

print (tags)

for file in lst:
    if file.endswith(".csv"):
        df = pd.read_csv("user_timeline_score/" + file, header=0, encoding="utf-8")
        df = df[df['hashtags'] != "[]"]
        print (df.shape)
        if df.shape[0] != 0:
            df_user = pd.DataFrame(np.zeros((1, len(tags)), dtype=np.float32), columns=tags)
            for i in range(df.shape[0]):
                tag_list = df.iat[i, 3]

                score = df.iat[i, 4]

                user_tags = tag_list[1:-1].split("*")
                for t in user_tags:
                    if t == u"":
                        break
                    df_user[t][0] = float(df_user[t][0])
                    df_user[t][0] += float(score)
            print ("-------")
            print (df_user)
            print ("-------")
            users.append(df_user)





