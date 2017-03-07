#! /usr/bin/env python3

#twitter bot rewritten in Python


from secrets import *
from random import randint
import json
from urllib.request import urlopen
#import tweepy

#auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#api = tweepy.API(auth)

randos = randint(100000000,100200719);

def find_by_rel(id):
    return "http://www.sixdegreesoffrancisbacon.com/relationships/{}.json".format(id)

def find_by_ppl(id):
    return "http://www.sixdegreesoffrancisbacon.com/people/{}.json".format(id)

def compose_tweet(id):
    url = find_by_rel(randos)
    data = json.loads(list(response)[0].decode('utf-8'))
    relationship_data = data["type_certainty_list"]
    if len(relationship_data) > 1:
        relationship_data = relationship_data[-1]
    else:
        relationship_data = relationship_data[0]

    conf = relationship_data[1]
    reltype = relationship_data[2]
    person1_id = data['person1_index']
    person2_id = data['person2_index']

    
def parse_confidence(conf):
    if conf >= 80:
        return 'certain'
    elif conf < 80 and conf >= 60:
        return 'very likely'
    elif conf < 60 and conf >= 40:
        return 'possible'
    elif conf < 40 and conf >= 20:
        return 'unlikely'
    else:
        return 'very unlikely'

print(url)
response = urlopen(url)
print(data)
person = find_by_ppl(randos)
print(person)
