import pandas as pd
import numpy as np
import json
import re
import os
import nltk

with open('adulting_tweets.json') as f:
    tweets = json.load(f)

#

# find all emojis
for tweet in tweets:
    tweet['emojis'] = re.findall(r'[\u263a-\U0001f645]', tweet['text'])

emojis = []
for tweet in tweets:
    emojis += tweet['emojis']

emoji_counts = pd.DataFrame({x: emojis.count(x) for x in emojis}.items(),
                            columns = ['emoji', 'appearances'])

n_emoji_tweets = 0
for tweet in tweets:
    if len(tweet['emojis']) > 0:
        n_emoji_tweets += 1

n_emoji_tweets/len(tweets)
