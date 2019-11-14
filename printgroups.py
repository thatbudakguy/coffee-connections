import json
import csv

with open('group7.json') as file:
    round7 = json.loads(file.read())

for group in round7:
    for name in group['names']:
        print(name + ',' + group['emails'][group['names'].index(name)])
    print('')
