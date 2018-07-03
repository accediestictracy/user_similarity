import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time



consumer_key = 'StL9clEvpKp1h0NSxEkP3h64X'
consumer_secret = 'Gzfk2ZkGN8ulOgKBI68bc84EDzSaCYqU6CZvHH7NZhYBGUq01i'
access_token = '789667055968452608-naAD770JLgQLYNHwr8HSlai5jvOQVZQ'
access_token_secret = 'xveyoP2e15fc40mKuqA3XJgzzIqbZRRWeTsu7ApZDIgvf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
list = open('/Users/tracywang/Downloads/Twitter-Sentiment-Analysis-master/venv1/userID.csv','w ')
if(api.verify_credentials):
    print("we successfully logged in")
    user = tweepy.Cursor(api.followers, screen_name="EmmaWatson").items()
    flag = 0
    while flag < 15:
        try:
            u = next(user)
            # list.write(u.screen_name + '\n')
            # print u.screen_name
            # if u.followers_count >=10:
            #     print u.followers_count
            if u.followers_count >= 50:
                list.write(u.screen_name + '\n')

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

#public_tweets = api.user_timeline('LeoDiCaprio')

#for tweet in public_tweets:
#   print tweet.text

