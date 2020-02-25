import pandas as pd
import numpy as np
import json
import re
import os
import nltk

with open('adulting_tweets.json') as f:
    tweets = json.load(f)

# clean data
nltk.download('punkt')

from contractions import CONTRACTION_MAP

def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):

    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

for tweet in tweets:
    tweet['clean_text'] = re.sub('[,\.\-\"\"]', '', tweet['text'].lower())
    tweet['clean_text'] = re.sub('’', "'", tweet['clean_text'])
    tweet['clean_text'] = re.sub('‘', "'", tweet['clean_text'])
    tweet['clean_text'] = expand_contractions(tweet['clean_text'])
    tweet['clean_text'] = nltk.word_tokenize(tweet['clean_text'])

text = []
for tweet in tweets:
    if not tweet['truncated']:
        text += tweet['clean_text']

text_filt = [word for word in text if word not in nltk.corpus.stopwords.words('english')]



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
