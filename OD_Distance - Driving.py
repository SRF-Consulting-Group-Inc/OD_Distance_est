import googlemaps
import os 
import numpy as np
import pandas as pd
import re
import csv
import _pickle as cPickle
from datetime import datetime


path = 'C:/Users/dgallen/Desktop/Python/OD_Distance_est'
os.chdir(path)
cwd = os.getcwd()
print(cwd)
files = os.listdir(path)

k = open('C:/Users/dgallen/Desktop/Python/k/New Text Document.txt','r').read()
OD = pd.read_csv('OD_set_auto.csv')
#OD = OD.set_index('TCode')
gmaps = googlemaps.Client(k)

OD['origin'] = [[OD['ox'][x],OD['oy'][x]] for x in range(OD.shape[0])]
OD['dest'] = [[OD['dx'][x],OD['dy'][x]] for x in range(OD.shape[0])]

OD_test = OD.iloc[:25]

DT = datetime.strptime('2018-10-3 07:00', '%Y-%m-%d %H:%M')
	
direct = gmaps.directions(origin = OD_test['origin'][1],
                      destination = OD_test['dest'][1],
                       mode = 'driving',
					   alternatives = True,
					   traffic_model = 'pessimistic',
					   departure_time = DT)

direct[1]['legs'][0]['steps'][5]['html_instructions']

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

cPickle.dump(direct, open('save.p', 'wb')) 


direct[1]['legs'][0]['duration_in_traffic']
direct[0]['legs'][0]['steps'][0]['html_instructions']
direct[0]['legs'][0]['steps'][0]

import cPickle
cPickle.dump(obj, open('save.p', 'wb')) 
obj = cPickle.load(open('save.p', 'rb'))


results = []
for x in range(OD_test.shape[0]):
           direct = gmaps.directions(origin = OD_test['origin'][1],
                       destination = OD_test['dest'][1],
                       mode = 'driving',
					   arrival_time = DT,
					   traffic_model = 'pessimistic')
           results.append(direct)

results[0][1]['legs'][0]['arrival_time']
results[0][0]['legs'][0]['steps'][1]['html_instructions']
results[0][0]['legs'][0]['steps'][1]['duration']['value']
results[1][0]['legs'][0]['departure_time']


arrival = []
departure = []
for idx, val in enumerate(results):
	if val == []:
		x = []
		y = []
	else:
		x = val[0]['legs'][0]['departure_time']['text']
		y = val[0]['legs'][0]['arrival_time']['text']
	departure.append(x)
	arrival.append(y)


res = []
for idx, val in enumerate(results):
	if val == []:
		x = []
	else:
		x = val[0]['legs'][0]['steps']
	res.append(x)



duration = []
direction = []
route = []
for idx, val in enumerate(res):
	if val == []:
		r = []
	else:
		r = val
	dur_list = []
	dir_list = []
	route_list = []
	for c, value in enumerate(r):
		dur = value['duration']['value']
		dir = value['html_instructions']
		if value['travel_mode'] == 'TRANSIT':
			route_list.append('Bus')
		else:
			route_list.append('Walk')
		dur_list.append(dur)
		dir_list.append(dir)
	duration.append(dur_list)
	direction.append(dir_list)
	route.append(route_list)

OD_test['Directions'] = [direction[x] for x in range(OD_test.shape[0])]
OD_test['Durations_sec'] = [duration[x] for x in range(OD_test.shape[0])]
#OD_test['Bus_route'] = [route[x] for x in range(OD_test.shape[0])]
OD_test['Final_Arrival'] = [arrival[x] for x in range(OD_test.shape[0])]
OD_test['Initial_Departure'] = [departure[x] for x in range(OD_test.shape[0])]

pa = []
for x in range(OD_test.shape[0]):
	if OD_test['Final_Arrival'][x] == []:
		p = []
	else:
		p = (datetime.strptime(OD_test['Final_Arrival'][x], '%H:%M%p') - datetime.strptime(OD_test['Initial_Departure'][x], '%H:%M%p')).seconds/60
	pa.append(p)
OD_test['Total_Trip_Duration_mins'] = [pa[x] for x in range(OD_test.shape[0])]

s = OD_test.apply(lambda x: pd.Series(x['Durations_sec']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'Duration (sec)'
s = s.reset_index()
t = OD_test.apply(lambda x: pd.Series(x['Directions']),axis=1).stack().reset_index(level=1, drop=True)
t.name = 'Direction'
t = t.reset_index().drop(['TCode'], axis = 1)
merged_items = s.join(t)

merge201_212 = OD_test[['Name','destCity','Final_Arrival','Initial_Departure','Total_Trip_Duration_mins']].join(merged_items.set_index('TCode'))

merge1_100
merge101_200
merge = merge1_100.append(merge101_200)
merge = merge.append(merge201_212)
merge.to_csv('OD_results_800.csv')