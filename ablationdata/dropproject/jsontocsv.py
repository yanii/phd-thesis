#!/usr/bin/python

import sys
import os
import json
import csv

jsonfilename = sys.argv[1]

with open(jsonfilename) as jsonfile:
    data = json.load(jsonfile)
jsonfile.close()

csvfile = open(os.path.splitext(jsonfilename)[0]+'.csv', 'w')
csv = csv.writer(csvfile)
csv.writerow(data[0].keys())
for row in data:
    csv.writerow(row.values())
csvfile.close()
