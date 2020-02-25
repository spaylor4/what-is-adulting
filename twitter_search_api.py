"""Script for implementing the Twitter Search API 
to generate a sample of tweets containing the word 'adulting'"""

import requests
import json

with open('./twitter_api_keys.json') as f:
    creds = json.load(f)
    
search_url = 'https://api.twitter.com/1.1/search/tweets.json'
search_headers = {'Authorization': 'Bearer ' + creds['ACCESS_TOKEN']}
search_params = {'q': 'adulting AND -RT AND -https://t.co', 
                 'lang': 'en', 'count': 100}

r = requests.get(search_url, headers = search_headers, params = search_params)

tweets = r.json()['statuses']

next_url = r.json()['search_metadata']['next_results']

#just sampling data for now, will update later for larger sample
for i in range(1,11):
    r_next = requests.get(search_url + next_url, headers = search_headers)
    tweets = tweets + r_next.json()['statuses']
    next_url = r_next.json()['search_metadata']['next_results']
    
with open('adulting_tweets.json', 'w', encoding='utf-8') as f:
    json.dump(tweets, f, ensure_ascii=False, indent=4)