import pandas as pd
import numpy as np
import json
import re
import os
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

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

# word frequency analysis
nltk.FreqDist(text_filt).most_common(25)

word_freq = pd.DataFrame(nltk.FreqDist(text_filt).most_common(25), columns=['word', 'frequency'])

plt.figure(figsize=(8, 5))
sns.set_style('white')
ax = sns.barplot(x = 'word', y = 'frequency', data = word_freq, color = 'lightblue')
ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
sns.despine()
sns.set(font_scale=2)

#collocations

bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = nltk.collocations.BigramCollocationFinder.from_words(text)
finder.apply_freq_filter(3)
finder.nbest(bigram_measures.pmi, 20)

trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = nltk.collocations.TrigramCollocationFinder.from_words(text)
finder.apply_freq_filter(3)
finder.nbest(trigram_measures.pmi, 20)

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
