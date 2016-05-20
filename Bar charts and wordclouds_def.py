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
import pandas as pd
import wordcloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pip

# Note: problems wordcloud solved after installing like this:
def install(package):
   pip.main(['install', 'wordcloud'])

install('wordcloud') 

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

variables = ['tweet', 'username','screenname','user_lang', 'lang', 'full_loc','user', 'name',  'location', 'friends_count','user_id', 'time_zone','lang', 'id_str', 'place', 'created_at', 'retweeted']
for var in variables:
    tweets[var] = [tweet.get(var, '') for tweet in tweets_data]

# Now we should be able to create some descriptive charts: 
# Firt try one describing the Top languages in which the tweets were written, 
# and then the Top 20 location from which the tweets were sent.
userlang = removed_tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
userlang[:5].plot(ax=ax, kind='bar', color='pink')

# look at locations of tweets
userloc = removed_tweets['location'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 20 locations', fontsize=15, fontweight='bold')
userloc[:20].plot(ax=ax, kind='bar', color='purple')

# Create Word cloud
words = ' '.join(removed_tweets['tweet'])

# remove URLs, RTs, and twitter handles
no_urls_no_tags = " ".join([word for word in words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                            ])

# Twitter symbol as mask
from scipy.misc import imread

twitter_mask = imread('C:/BIOS6640 project/twitter_mask.png', flatten=True)

wc = WordCloud(font_path='C:/BIOS6640 project//Library/Fonts/CabinSketch-Bold.ttf',                 
                      stopwords=STOPWORDS,
                      background_color='white',
                      width=3600,
                      height=2800,
                      mask=twitter_mask
            ).generate(no_urls_no_tags)

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('C:/BIOS6640 project/my_twitter_wordcloud_7.png', dpi=300)
plt.show()

# U.S. mask
us_mask= imread('C:/BIOS6640 project/us-mask-white.png', flatten=True)

wc = WordCloud(                    
                      stopwords=STOPWORDS,
                      background_color='black',
                      width=1800,
                      height=1400,
                      mask=us_mask
            ).generate(no_urls_no_tags)

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('C:/BIOS6640 project/us_wordcloud_.png', dpi=300)
plt.show()







