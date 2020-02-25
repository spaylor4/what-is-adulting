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
