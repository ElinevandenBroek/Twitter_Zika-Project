# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:17:35 2016

@author: vandenel
"""
import pip
pip.main(['install','tweepy'])


#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "15032066-RekyySmAhK0eNkSi4ErMqxDYhjTfIV5j7C2OCT1mo"
access_token_secret = "X89LRlTO28wGqPWU3RMrInZcvbsqMb0fUyTL7akPz9kkN"
consumer_key = "TVsxn95oHyNzm9KNGYQ8k8f0p"
consumer_secret = "HwPUFKw1btNMwJ2R12ILrlS4m0Bw2PVnLft7iMYRuEQlEPCqSR"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print data
        with open('C/BIOS6640 project/Zika_mentions_Twitter.txt','a') as tf:             
            tf.write(data)
        return True

    def on_error(self, status): 
        #print status 
        if __name__ == '__main__':

        #This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keyword 'Zika'
        stream.filter(track=['zika'])
        


