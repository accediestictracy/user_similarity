#!/usr/bin/env python
# encoding: utf-8
import tweepy
import csv

consumer_key = 'StL9clEvpKp1h0NSxEkP3h64X'
consumer_secret = 'Gzfk2ZkGN8ulOgKBI68bc84EDzSaCYqU6CZvHH7NZhYBGUq01i'
access_token = '789667055968452608-naAD770JLgQLYNHwr8HSlai5jvOQVZQ'
access_token_secret = 'xveyoP2e15fc40mKuqA3XJgzzIqbZRRWeTsu7ApZDIgvf'


def get_all_tweets(screen_name):
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
    while len(new_tweets) > 0 and max_count <= 5:
        print ("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
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
            print ("sSSSSsss")
            print (type(raw_tags[0]["text"]))
            print (raw_tags[0]["text"])
            return raw_tags[0]["text"].encode("utf-8")

    outtweets = [[tweet.id_str, tweet.user.screen_name, tweet.created_at, parse_hash_tags(tweet.entities["hashtags"]),
                  tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["tweet_id","screen_name", "created_at","hashtags", "text"])
        writer.writerows(outtweets)
    pass


if __name__ == '__main__':

    with open('/Users/tracywang/Downloads/Twitter-Sentiment-Analysis-master/venv1/userID.csv', 'rb') as f:
        ID = csv.reader(f)
        for row in ID:
            # 这里运用了错误查询机制，遇到用户ID出现问题时，可以跳过
            try:
                print (row[0])
                get_all_tweets(row[0])
            except tweepy.TweepError as e:
                print ('Failed to run the command on that user, Skipping...')
            except IndexError as e:
                print ('List index out of range, Skipping...')
                continue


