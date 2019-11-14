import json
import csv


with open('database.json') as file:
    db = json.loads(file.read())

db_id = len(db)+1
db_names = [person['name'] for person in db]
next_round_ids = []

# update the database with the last round groupings
def update_db(db, filename):
    with open(filename) as file:
        groups = json.loads(file.read())
        for row in groups:
            for id in row['group']:
                db[id-1]['connections'] += row['group']
                db[id-1]['connections'].remove(id)
    return db

# get subset of database for current signups
with open('round7.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for i, row in enumerate(reader):
        if i > 0:
            if row[2] not in db_names:
                next_round_ids.append(db_id)
                db.append({
                    'id': db_id,
                    'name': row[2],
                    'location': row[3],
                    'department': row[4],
                    'class': row[5],
                    'email': row[1],
                    'connections': []
                })
                db_id += 1
            else:
                next_round_ids.append(db_names.index(row[2])+1)

#updated_db = update_db(db, 'round5')
#print(json.dumps(updated_db, indent=4))

current_signups = [db[id - 1] for id in next_round_ids]
print(json.dumps(current_signups, indent=4))
