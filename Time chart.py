import pandas as pd
import json
import pandas

# First we want to create a path for the file with the tweets
tweets_data_path = 'C:/BIOS6640 project/Zika_mentions_Twitter.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
tweet_set = pd.DataFrame(tweets_data)
# Look at occurences in dataset (.txt)
tweet_set.isnull().sum()
    
# Transforms our list to a data frame for specific variables. See the 'tweet'
# dictionary file to reference specific elements in the data frame creation
tweets = pd.DataFrame()

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


# Again add the info, this time more variables
tweets['text'] = map(lambda tweet:tweet['text'] if 'text' in tweet \   else ' ', tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'] if 'text' in tweet \     else ' ', tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] \     if 'text' in tweet and tweet['place'] != None else None, tweets_data)
tweets['tweet_time'] = map(lambda tweet: tweet['created_at'] \     if 'text' in tweet else ' ', tweets_data)
tweets['name'] = map(lambda tweet: tweet['user']['name'] if 'text' in tweet \     else ' ', tweets_data)
tweets['handle'] = map(lambda tweet: tweet['user']['screen_name'] \     if 'text' in tweet else ' ', tweets_data)
# Location 
tweets['geo_available'] = map(lambda tweet: tweet['user']\     ['geo_enabled'] if 'text' in tweet else ' ', tweets_data)
tweets['coordinates'] = map(lambda tweet: tweet['coordinates'] \     if 'text' in tweet else ' ', tweets_data)
tweets['geo'] = map(lambda tweet: tweet['geo'] \     if 'text' in tweet else ' ', tweets_data)
tweets['place'] = map(lambda tweet: tweet['place'] \     if 'text' in tweet else ' ', tweets_data)
tweets['coordinates'] = map(lambda tweet: tweet['coordinates'] \     if 'text' in tweet else ' ', tweets_data)
tweets['location'] = map(lambda tweet: tweet['user']\     ['location'] if 'text' in tweet else ' ', tweets_data)
tweets['time_zone'] = map(lambda tweet: tweet['user']\     ['time_zone'] if 'text' in tweet else ' ', tweets_data)


# Add columns to the df
tweets.columns.values

dates_zika = []
for line in tweets_file:
    tweet = json.loads(line)
    terms_hash = [term for term in (tweet['text']) if term.startswith('#')]
    # track when the hashtag is mentioned
    if '#zika' in terms_hash:
        dates_zika.append(tweet['created_at'])
 
# a list of "1" to count the hashtags
ones = [1]*len(dates_zika)
# the index of the series
idx = pandas.DatetimeIndex(dates_zika)
# the actual series (at series of 1s for the moment)
zika = pandas.Series(ones, index=idx)
 
# Resampling / bucketing
per_minute = zika.resample('1Min', how='sum').fillna(0)

import vincent
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

# in command prompt:  python -m SimpleHTTPServer 8888

# Now we can retrieve the time plot

# For the other plots we go to R
df = tweets
df.to_csv('zika_project.csv', encoding='utf-8')  