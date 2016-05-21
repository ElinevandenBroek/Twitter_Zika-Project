"""
Created on Thu May 12 18:16:14 2016
This code is for BIOS 6640 Final Project

Thanks to Caroline's fetched tweets text file for the analysis.
I used 3 websites for inspiration:
https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
http://adilmoujahid.com/posts/2014/07/twitter-analytics/
http://sebastianraschka.com/Articles/2014_twitter_wordcloud.html

@author: vandenel
"""
# Loading packages needed for analysis
import pip
import json
import numpy as np
import pandas
import pandas as pd
import re
import vincent
from collections import Counter
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt

tweets_data_path = 'C:/BIOS6640 project/Zika_mentions_Twitter.txt'

tweets_file = open(tweets_data_path, "r")

tweets = []

for line in open('C:/BIOS6640 project/Zika_mentions_Twitter.txt'):
  try: 
    tweets.append(json.loads(line))
  except:
    pass

# Check amount of tweets:
print len(tweets)

# Look at a single tweet:
tweet = tweets[0]
print tweet

# Check all keys
print tweet.keys()
print tweet['user'].keys() 
print tweet['entities']
  
print tweet['geo_data'] # None

# Now, before looking at common words and look at patterns and sentiments, we want to create a pre-processing chain 
# taking into account signs like @, URLs or emoticons
# borrowed from https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/ 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
   r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
    
       
# So now we want to get rid of useless signs
punctuation = list(string.punctuation)
stop2 = punctuation + ['RT', 'via']

terms_stop2 = [word for word in (tweet['text'])if word not in stop2]


# Now we print the top 10:
count_all = Counter() 
count_all.update(terms_stop)
# Print the first 5 most frequent words
print(count_all.most_common(5))

# Count hashtags only
terms_hash = [term for term in preprocess(tweet['text'])  if term.startswith('#')]
# Count terms only (no hashtags, no mentions)

terms_only = [term for term in (tweet['text']) if term not in stop and
              not term.startswith(('#', '@'))] 

print (terms_hash)
print (terms_only)
  
from nltk import bigrams 
terms_bigram = bigrams(terms_stop)
print (terms_bigram)
  

# Print out
count_all.update(terms_only)
# Print the first 5 most frequent words
print(count_all.most_common(5))

# Print out
count_all.update(terms_hash)
# Print the first 5 most frequent words
print(count_all.most_common(5))


word_freq = count_all.most_common(5)

labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')


'''<html>  
<head>    
    <title>Vega Scaffold</title>
    <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
    <script src="http://d3js.org/topojson.v1.min.js"></script>
    <script src="http://d3js.org/d3.geo.projection.v0.min.js" charset="utf-8"></script>
    <script src="http://trifacta.github.com/vega/vega.js"></script>
</head>
<body>
    <div id="vis"></div>
</body>
<script type="text/javascript">
// parse a spec and create a visualization view
function parse(spec) {
  vg.parse.spec(spec, function(chart) { chart({el:"#vis"}).update(); });
}
parse("term_freq.json");
</script>
</html>'''

#save
bar.to_json('term_freq.json', html_out=True, html_path='chart.html')







