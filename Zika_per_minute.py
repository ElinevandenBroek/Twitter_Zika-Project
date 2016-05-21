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
import json
import numpy as np
import pandas
import pandas as pd
import pip
import vincent

# First we want to create a path for the file with the tweets
tweets_data_path = 'C:/BIOS6640 project/Zika_mentions_Twitter.txt'

# Now we need to the data in the text file into a data frame so we can run analysis
tweets_data = []
keywords = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

print len(tweets_data)

# Create dataframe
tweets = pd.DataFrame()

# Create variables to use for analysis
tweets['tweet'] = map(lambda tweet: tweet['text'] if 'text' in tweet else np.nan, tweets_data)
tweets['created_at'] = map(lambda tweet: tweet['created_at'] if 'created_at' in tweet else np.nan, tweets_data)
tweets['user_id'] = map(lambda tweet: tweet['user']['id'] if 'user' in tweet else np.nan, tweets_data)
tweets['id_str'] = map(lambda tweet: tweet['user']['id_str'] if 'user' in tweet else np.nan, tweets_data)
tweets['username'] = map(lambda tweet: tweet['user']['name'] if 'user' in tweet else np.nan, tweets_data)
tweets['screen_name'] = map(lambda tweet: tweet['user']['screen_name'] if 'user' in tweet else np.nan, tweets_data)
tweets['location'] = map(lambda tweet: tweet['user']['location'] if 'user' in tweet else np.nan, tweets_data)
tweets['friends_count'] = map(lambda tweet: tweet['user']['friends_count'] if 'user' in tweet else np.nan, tweets_data)
tweets['user_lang'] = map(lambda tweet: tweet['user']['lang'] if 'user' in tweet else np.nan, tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'] if 'lang' in tweet else np.nan, tweets_data)
tweets['full_loc'] = map(lambda tweet: tweet['place'] if 'place' in tweet else np.nan, tweets_data)
tweets['time_zone'] = [tweet["user"]['time_zone'] if "user" in tweet and tweet["user"]['time_zone']
                       else np.nan for tweet in tweets_data]   
# Get rid of missing data
removed_tweets = tweets[~tweets['tweet'].apply(lambda x: isinstance(x,float))]

# Add columns to the df
tweets.columns.values


dates_zika = []
tweets_file = open(tweets_data_path, "r")

for line in tweets_file:
        tweet = json.loads(line)
        if 'zika' in tweet:
            dates_zika.append(tweet['created_at'])
 
# a list of "1" to count the hashtags
ones = [1]*len(dates_zika)
print ones
# the index of the series
idx = pandas.DatetimeIndex(dates_zika)
# the actual series (at series of 1s for the moment)
zika = pandas.Series(ones, index=idx)
 
# Resampling / bucketing
per_minute = zika.resample('1Min', how='sum').fillna(0)

time_chart = vincent.Line(zika)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json')

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
parse("time_chart.json");
</script>
</html>'''

#save
time_chart.to_json('time_chart.json', html_out=True, html_path='chart.html')

import SimpleHTTPServer
import SocketServer

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

# Create table of engagement / activity
import pandas as pd
import os
import time
from datetime import datetime

df = pandas.DataFrame(columns = ['tweet', 'username','screenname','user_lang', 'lang', 'full_loc','user', 'name',  'location', 'friends_count','user_id', 'time_zone','lang', 'id_str', 'place', 'created_at', 'retweeted'])
def index(tweets, wordList):
    'string, list(string) ==> string & int, returns an index of words with the line number\
    each word occurs in'
    indexDict = {['tweet', 'username','screenname','user_lang', 'lang', 'full_loc','user', 'name',  'location', 'friends_count','user_id', 'time_zone','lang', 'id_str', 'place', 'created_at', 'retweeted']}
    res = []
    tweets_file = open(tweets_data_path, "r")
    count = 0
    line = tweets_file.readline()
    while line != '':
        count += 1
        for word in wordList:
            if word in line:
                #indexDict[word] = [count]
                print(word, count)
        line = tweets_file.readline()
        # return indexDict
   