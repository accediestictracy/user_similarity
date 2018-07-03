#!/usr/bin/env python
# encoding: utf-8


import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

consumer_key = 'StL9clEvpKp1h0NSxEkP3h64X'
consumer_secret = 'Gzfk2ZkGN8ulOgKBI68bc84EDzSaCYqU6CZvHH7NZhYBGUq01i'
access_token = '789667055968452608-naAD770JLgQLYNHwr8HSlai5jvOQVZQ'
access_token_secret = 'xveyoP2e15fc40mKuqA3XJgzzIqbZRRWeTsu7ApZDIgvf'



# ---------------------------------------

import tweepy
import csv


def get_at_most_300_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # 初始化一个数字来存储所有的tweets
    alltweets = []

    new_tweets = api.user_timeline(screen_name=screen_name, count=100)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    max_count = 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and max_count <= 3:
        print ("getting tweets before %s" % (oldest))

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=100, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        max_count += 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv

    def parse_hash_tags(raw_tags):
        if len(raw_tags) == 0:
            return []
        else:

            return raw_tags[0]["text"].encode("utf-8")
    def outtweets():
        outtweets = [[tweet.id_str, tweet.user.screen_name, tweet.created_at, parse_hash_tags(tweet.entities["hashtags"]),
                  tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv
    with open('/Users/tracywang/Downloads/Twitter-Sentiment-Analysis-master/venv1/user_timeline/%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["tweet_id", "screen_name", "created_at", "hashtags", "text"])
        writer.writerows(outtweets)
    pass



# -----------------------------------
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
list = open('/Users/tracywang/Downloads/Twitter-Sentiment-Analysis-master/venv1/userID_new.csv', 'a')
if (api.verify_credentials):
    print("we successfully logged in")
    user = tweepy.Cursor(api.followers, screen_name="EmmaWatson").items()
    flag = 0



    while flag < 1000:  #tian hen da de shu zi
        try:
            u = next(user)
            # list.write(u.screen_name + '\n')
            # print u.screen_name
            # if u.followers_count >=10:
            #     print u.followers_count
            if u.followers_count >= 50:
                list.write(u.screen_name + '\n')

                #  output tweets to csv file
                get_at_most_300_tweets(u.screen_name)

                flag += 1
            else:
                u = next(user)
        except:
            time.sleep(15 * 60)
            print("we got a timeout")
            u = next(user)
            list.write(u.screen_name + '\n')
            flag += 1
list.close()

# public_tweets = api.user_timeline('LeoDiCaprio')

# for tweet in public_tweets:
#   print tweet.text

if __name__ == '__main__':
    # get_at_most_300_tweets('joliestweet')
    get_at_most_300_tweets('EmmaWatson')


