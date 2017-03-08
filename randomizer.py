#! /usr/bin/env python3

#twitter bot rewritten in Python


from secrets import *
from random import randint
import json
from urllib.request import urlopen
import tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

randos = randint(100000000,100200719);

def find_by_rel(id):
    return "http://www.sixdegreesoffrancisbacon.com/relationships/{}.json".format(id)

def find_by_ppl(id):
    return "http://www.sixdegreesoffrancisbacon.com/people/{}.json".format(id)

def get_person_name(id):
    url = find_by_ppl(id)
    response = urlopen(url)
    data = json.loads(list(response)[0].decode('utf-8'))
    name = data['display_name']
    return name
    
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

def compose_tweet(id):
    url = None
    while url == None:
        try:
            url = find_by_rel(randos)
        except HTTPError:
            pass
    response = urlopen(url)
    data = json.loads(list(response)[0].decode('utf-8'))
    relationship_data = data["type_certainty_list"]
    if len(relationship_data) > 1:
        relationship_data = relationship_data[-1]
    else:
        relationship_data = relationship_data[0]

    conf = relationship_data[1]
    confidence = parse_confidence(conf)
    reltype = relationship_data[2]
    person1_id = data['person1_index']
    person1_name = get_person_name(person1_id)
    person2_id = data['person2_index']
    person2_name = get_person_name(person2_id)
    tweet = "It is {0} that {1} {2} {3}. See their shared network: http://sixdegreesoffrancisbacon.com/?id={4}&id2={5}&confidence=60,100&date=1500,1700&table=no".format(confidence, person1_name, reltype, person2_name, person1_id, person2_id)
    return tweet


tweet = compose_tweet(randos)
api.update_status(tweet)

