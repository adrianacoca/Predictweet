import os
from dotenv import load_dotenv
import requests
import requests_oauthlib
import json
import pandas as pd
import numpy as np
from collections import Counter

def get_auth():
    load_dotenv()
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_SECRET = os.getenv("ACCESS_SECRET")
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
    return my_auth
def get_tweets(user):
    my_auth = get_auth()
    url = f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={user}&count=100&tweet_mode=extended'
    response = requests.get(url, auth=my_auth, stream=True)
    print(url, response)
    return response.json()

def create_data(user_t):
    id_ = []
    retweet_count = []
    tweet = []
    time = []
    for i in range(len(user_t)):
        id_.append(user_t[i]["id_str"])
        retweet_count.append(user_t[i]["retweet_count"])
        time.append(user_t[i]['created_at'])
        try:
            tweet.append(user_t[i]['retweeted_status']['full_text'])
        except: 
            tweet.append(user_t[i]["full_text"])
    d = {"id":id_, "time":time, "tweet": tweet, "retweets":retweet_count}
    data = pd.DataFrame(data = d)
    return data

def get_replies(user, tweet_id):
    my_auth = get_auth()
    url = f'https://api.twitter.com/1.1/search/tweets.json?q=%40{user}&count=100&tweet_mode=extended&in_reply_to_status_id_str={tweet_id}'
    response = requests.get(url, auth=my_auth, stream=True)
    responses =  response.json()
    tweet_responses = []
    for i in range(len(responses["statuses"])):
        try: 
            tweet_responses.append(responses["statuses"][i]['retweeted_status']['full_text'])
        except: 
            tweet_responses.append(responses["statuses"][i]["full_text"])
    return tweet_responses

def add_replies(user, data):
    responses = []
    for id_ in list(data["id"]):
        r = get_replies(user, id_)
        responses.append(r)
    return responses

def get_hashtag_string(string):
    x = re.findall("#\w*", string)
    h = []
    for i in x:
        result = re.sub("#", "", i)
        h.append(result)
    return h

def avg(lst):
    return sum(lst) / len(lst) 

def get_hashtag(data):
    hashtags = []
    for i in range(len(data["responses"])):
        tweet_hashtags = []
        for l in range(len(data["responses"][i])):
            tweet_hashtags.append(get_hashtag_string(data["responses"][i][l]))
        hashtags.append([h for i in tweet_hashtags for h in i])
    data["hashtags"] = hashtags
    hashtags_count = []
    for i in range(len(data["hashtags"])):
        hashtags_count.append(dict(Counter(data["hashtags"][i])))
    h = set([w for l in data["hashtags"] for w in l])
    all_hashtags = {}
    for w in h:
        all_hashtags[w]=[]
    for d in range(len(hashtags_count)):
        l = list(hashtags_count[d].items())
        s = data["sentiments"][d]
        for i in range(len(l)):
            key = l[i][0]
            value = l[i][1]
            for n in range(value):
                all_hashtags[key].append(s)
    topics = pd.DataFrame(all_hashtags.items(), columns=['Hashtag', 'Sentiment List'])
    topics["Average Sentiment"] = topics['Sentiment List'].apply(avg)
    topics.sort_values(by='Average Sentiment', ascending=True, inplace=True)
    mn = topics["Average Sentiment"].min()-0.01
    topics["plot"] = list(topics["Average Sentiment"]-mn)
    return topics
