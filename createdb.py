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
                'email': row[1],
                'connections': []
            })

with open('met.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        name = row[0]
        person = [person for person in data if person['name'] == name]
        if len(person) > 0:
            connection_names = [c for c in row[1:] if c != ""]
            connection_ids = [person['id'] for person in data if person['name'] in connection_names]
            data[person[0]['id'] - 1]['connections'] = connection_ids

print(json.dumps(data, indent=4))
