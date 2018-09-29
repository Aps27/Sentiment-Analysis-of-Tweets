'''
	
	SENTINAL ANALYSIS
  ---------------------	

Sentiment analysis is the process of 'computationally' determining whether a piece of string (as a part of a comment, 
writing or a casual conversation) is positive, negative or nuetral. It is also known as opinion mining, deriving the
opinion or attitude of the speaker.

This version is a bsic version without machine learning or advanced python libraries. The upgraded version
will be put up soon. Python 3 is preffered

1. sudo pip install --upgrade pip 
2. sudo pip install tweepy  (for colllecting tweets) or pip3 install tweepy
3. pip install aylien-apiclient   (text analysis API, The AYLIEN Text Analysis API is a package of Natural
                                  Language Processing and Machine Learning-powered APIs for analyzing and 
                                  extracting various kinds of information from textual content.)
4. sudo python -m pip install -U matplotlib  (python visualization library) also sudo apt-get install python-tk (paints in tkinter app)
5. Get twitter access key and Api and Aylien API key

'''

import sys
import csv
import tweepy
import matplotlib.pyplot as plt

from collections import Counter
from aylienapiclient import textapi


## Twitter credentials
consumer_key = " "
consumer_secret = " "
access_token = " "
access_token_secret = " "

## AYLIEN credentials
application_id = " "
application_key = " "

## Tweepy API object instatiation
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

## AYLIEN Text API object instantiation
client = textapi.Client(application_id, application_key)

## Identify subject of search
query = raw_input("What subject of tweets do you want to analyze? \n")
number = input("How many Tweets do you want to analyze? \n") # maximum if 100 tweets limited by Twitter API

tweets = api.search(      # Returns a collection of relevant Tweets matching a specified query. JSON format
   lang="en",
   q=query + " -rt",
   count=number,		   
   result_type="popular"   
)

'''
The search query can also include geocode within a given radius of the given latitude/longitude. 
The location is preferentially taking from the Geotagging API.
The result type can also include recent/ mixed/ popular
'''

print("\n\n*** Successfully gathered Tweets !!! *** \n")

## open a csv file to store the Tweets and their sentiment 
file_name = 'Sentiment Analysis of {} Tweets About {}.csv'.format(number, query) #csv format

print("*** Opening an excel sheet to store the results of your sentiment analysis... *** \n")

with open(file_name, 'w') as csvfile:
   csv_writer = csv.DictWriter(                # DictWriter bcoz we need the data mapped into a dict whose keys are given by the optional fieldnames parameter
       f=csvfile,
       fieldnames=["Tweet", "Sentiment"]       # Table format
   )
   csv_writer.writeheader()                    # Writes a row with the field names


## tidy up the Tweets and send each to the AYLIEN Text API
   for c, tweets in enumerate(tweets, start=1):
       tweet = tweets.text
       tidy_tweet = tweet.strip().encode('ascii', 'ignore')

       if len(tweet) == 0:   # empty tweets are a waste of time
           print('Empty Tweet')
           continue

       response = client.Sentiment({'text': tidy_tweet})  #inbuilt Sentiment function
       csv_writer.writerow({
           'Tweet': response['text'],
           'Sentiment': response['polarity']
       })

       print("Analyzing Tweet {} ...".format(c))

## count the data in the Sentiment column of the CSV file 
with open(file_name, 'r') as data:
   counter = Counter()
   for row in csv.DictReader(data):
       counter[row['Sentiment']] += 1

   positive = counter['positive']
   negative = counter['negative']
   neutral = counter['neutral']

## declare the variables for the pie chart, using the Counter variables for "sizes"
colors = ['green', 'red', 'grey']
sizes = [positive, negative, neutral]
labels = 'Positive', 'Negative', 'Neutral'

## use matplotlib to plot the chart
plt.pie(
   x=sizes,
   shadow=True,
   colors=colors,
   labels=labels,
   startangle=90
)

plt.title("Sentiment of {} Tweets about {}".format(number, query))
plt.show()
