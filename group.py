import json
from random import shuffle

def make_groups(db):
    groups = []
    # pop() and shuffle() are destructive, so make two copies
    lookup = db.copy()
    db = db.copy()
    shuffle(db)
    while len(db) > 2:
        group = ()
        # pick an initial person
        leader = db.pop(0)
        group += (leader['id'],)
        # find someone they haven't been in a group with and add them to the group
        possible_matches = [person for person in db if person['id'] not in leader['connections']]
        for match in possible_matches:
            match['score'] = compute_pair_score(leader['id'], match['id'], lookup)
        # best matches sorted first
        possible_matches.sort(key=lambda match:match['score'])
        second_person = db.pop(db.index(possible_matches[0]))
        group += (second_person['id'],)
        # find a third person who hasn't been in a group with either of those two people and add them
        all_met = leader['connections'] + second_person['connections']
        possible_matches = [person for person in db if person['id'] not in all_met]
        for match in possible_matches:
            match['score'] = compute_group_score((leader['id'], second_person['id'], match['id']), lookup)
        possible_matches.sort(key=lambda match:match['score'])
        third_person = db.pop(db.index(possible_matches[0]))
        group += (third_person['id'],)
        groups.append(group)
    if len(db) > 0:
        # append remaining people as group, if any
        last_people = [person['id'] for person in db]
        group = tuple(last_people)
        groups.append(group)
    return groups

def named_groups(groups, db):
    named_groups = []
    for group in groups:
        names = tuple([person['name'] for person in db if person['id'] in group])
        named_groups.append(names)
    return named_groups

def compute_pair_score(id1, id2, db):
    person1 = [person for person in db if person['id'] == id1][0]
    person2 = [person for person in db if person['id'] == id2][0]
    score = 0
    if person1['department'] == person2['department']:
        score += 5
    if person1['location'] == person2['location']:
        score += 3
    if person1['class'] == person2['class']:
        score += 1
    return score

def compute_group_score(group, db):
    if len(group) == 1:
        return 0
    if len(group) == 2:
        return compute_pair_score(group[0], group[1], db)
    else:
        score = 0
        score += compute_pair_score(group[0], group[1], db)
        score += compute_pair_score(group[1], group[2], db)
        score += compute_pair_score(group[2], group[0], db)
        return score

# load database
with open('database.json') as file:
    db = json.loads(file.read())

groups = make_groups(db)

print([compute_group_score(group, db) for group in groups])