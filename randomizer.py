#! /usr/bin/env python3

#twitter bot rewritten in Python


from secrets import *
from random import randint
import json
from urllib.request import urlopen



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

randos = randint(100000000,100200719);

def find_by_rel(id):
    return "http://www.sixdegreesoffrancisbacon.com/relationships/{}.json".format(id)

def find_by_ppl(numb):
    print("http://www.sixdegreesoffrancisbacon.com/people/{}.json".format(numb))


url = find_by_rel(randos)
print(url)
response = urlopen(url)
data = json.loads(list(response)[0].decode('utf-8'))
print(data)
find_by_ppl(randos)
