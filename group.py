import json
import pprint
from random import shuffle

def make_groups(db):
    groups = []
    # pop() and shuffle() are destructive, so make two copies
    lookup = db.copy()
    db = db.copy()
    try:
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
    except IndexError:
        return make_groups(lookup)

def named_groups(groups, db):
    named_groups = []
    for group in groups:
        names = tuple([person['name'] for person in db if person['id'] in group])
        named_groups.append(names)
    return named_groups

def email_groups(groups, db):
    email_groups = []
    for group in groups:
        emails = tuple([person['email'] for person in db if person['id'] in group])
        email_groups.append(emails)
    return email_groups

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

def get_person(id, db):
    return db[id - 1]

def has_met(id1, id2, db):
    return id1 in get_person(id2, db)['connections']

def group_is_valid(group, db):
    if has_met(group[0], group[1], db):
        return False
    if has_met(group[1], group[2], db):
        return False
    if has_met(group[2], group[0], db):
        return False
    return True

def set_group(ids, db):
    group = tuple([person for person in db if person['id'] in ids])
    # remove them from the db
    for person in group:
        db.pop(db.index(person))
    # return the ids
    return [person['id'] for person in group]

# load database
with open('round7.json') as file:
    db = json.loads(file.read())

groups = make_groups(db)
named_groups = named_groups(groups, db)
email_groups = email_groups(groups, db)

output = []
pp = pprint.PrettyPrinter()

for i, group in enumerate(groups):
    output.append({
        'group': group,
        'names': named_groups[i],
        'emails': email_groups[i],
        'score': compute_group_score(group, db)
    })

print(json.dumps(output, indent=4))
