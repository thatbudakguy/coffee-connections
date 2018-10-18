import json
import csv

data = []

with open('round5.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for i, row in enumerate(reader):
        if i > 0:
            data.append({
                'id': i,
                'name': row[2],
                'location': row[3],
                'department': row[4],
                'class': row[5],
                'connections': []
            })

with open('met.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        name = row[0]
        person = list(filter(lambda person: person['name'] == name, data))
        if len(person) > 0:
            connection_names = [c for c in row[1:] if c != ""]
            connection_ids = list(map(lambda person: person['id'], filter(lambda person: person['name'] in connection_names, data)))
            data[person[0]['id'] - 1]['connections'] = connection_ids

print(json.dumps(data, indent=4))
