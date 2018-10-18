import json
from random import shuffle

# load database
with open('database.json') as file:
    db = json.loads(file.read())

backup = db

# create empty groups
groups = []

# randomize the order
shuffle(db)

while len(db) > 3:
    # make a group
    group = []
    # pick an initial person
    leader = db.pop(0)
    # print('leader is' + leader['name'])
    group.append(leader['id'])
    # find someone they haven't been in a group with and add them to the group
    possible_matches = list(filter(lambda person: person['id'] not in leader['connections'], db))
    # print('first match is' + possible_matches[0]['name'])
    second_person = db.pop(db.index(possible_matches[0]))
    group.append(second_person['id'])
    # find a third person who hasn't been in a group with either of those two people
    all_met = leader['connections'] + second_person['connections']
    possible_matches = list(filter(lambda person: person['id'] not in all_met, db))
    third_person = db.pop(db.index(possible_matches[0]))
    group.append(third_person['id'])
    groups.append(group)

print(json.dumps(groups))