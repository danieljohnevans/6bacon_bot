#! /usr/bin/env python3

#twitter bot rewritten in Python


from secrets import *
from random import randint
import json, tweepy, urllib2



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

randos = randint(100000000,100200719);

def find_by_rel(id):
    print("http://www.sixdegreesoffrancisbacon.com/relationships/{}.json".format(id))

def find_by_ppl(numb):
    print("http://www.sixdegreesoffrancisbacon.com/people/{}.json".format(numb))


url = find_by_rel(randos)
#url = "http://www.sixdegreesoffrancisbacon.com/relationships/100164544.json"
response = urllib2.urlopen(url)
data = json.loads(response.read())
print(data)
find_by_ppl(randos)
