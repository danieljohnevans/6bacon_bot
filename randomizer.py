#! /usr/bin/env python3

#twitter bot rewritten in Python


from random import randint, choice
import json
from urllib.request import urlopen
from urllib.error import HTTPError
from json.decoder import JSONDecodeError
import tweepy

CONSUMER_KEY          = "8VZQBLdmRXTiQQTNEfdqtTqIe"
CONSUMER_SECRET       = "anPXzjrK0N3L24NXO0TgS0ER4fujYzc3O6ACfXz7BqRgmf3uQZ"
ACCESS_TOKEN         = "727875481253588992-jViKSFJB4ANZizbKqUH89D4BAtemvYZ"
ACCESS_TOKEN_SECRET   = "IOZIIS7xxXJK5WKzEmHMcH1wBPmr9GCVlAZm4JxySKF3j"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


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

def compose_rel_tweet():
    response = None
    while response == None:
        try:
            id = randint(100000000,100200719)
            url = find_by_rel(id)
            response = urlopen(url)
        except HTTPError:
            pass
    data = json.loads(list(response)[0].decode('utf-8'))
    relationship_data = data["type_certainty_list"]
    if len(relationship_data) > 1:
        relationship_data = relationship_data[-1]
    else:
        relationship_data = relationship_data[0]

    conf = int(relationship_data[1])
    confidence = parse_confidence(conf)
    reltype = relationship_data[2]
    person1_id = data['person1_index']
    person1_name = get_person_name(person1_id)
    person2_id = data['person2_index']
    person2_name = get_person_name(person2_id)
    tweet = "6Bacon is {0}% certain that {1} {2} {3}. See their shared network: http://sixdegreesoffrancisbacon.com/?id={4}&id2={5}&confidence={0},100&date=1500,1700&table=no".format(conf, person1_name, reltype, person2_name, person1_id, person2_id)
    return tweet

def compose_person_tweet():
    response = None
    data = None
    while response == None or data == None:
        try:
            id = randint(10000001, 10054877)
            url = find_by_ppl(id)
            response = urlopen(url)
            data = json.loads(list(response)[0].decode('utf-8'))
        except (HTTPError, JSONDecodeError) as e:
            pass
    name = data['display_name'].strip()
    birthtype = parse_year_type(data['birth_year_type'])
    birthyear = data['ext_birth_year']
    deathtype = parse_year_type(data['death_year_type'])
    deathyear = data['ext_death_year']
    hist_sig = data['historical_significance'].strip()
    tweet = "{0}, {1}, was born {2} {3} and died {4} {5}. See the network: http://sixdegreesoffrancisbacon.com/people/{6}".format(name, hist_sig, birthtype, birthyear, deathtype, deathyear, id)
    return tweet

def parse_year_type(ytype):
    if ytype == 'IN':
        return 'in'
    elif ytype == 'BF':
        return 'before'
    elif ytype == 'AF':
        return 'after'
    elif ytype == 'CA':
        return 'circa'
    elif ytype == 'BF/IN':
        return 'before or in'
    elif ytype == 'AF/IN':
        return 'after or in'

coinflip = choice([0,1])
if coinflip == 0:
    tweet = compose_rel_tweet()
else:
    tweet = compose_person_tweet()

api.update_status(tweet)
# print(tweet)
