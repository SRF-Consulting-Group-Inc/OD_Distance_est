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

k = open('C:/Users/dgallen/Desktop/Python/k/New Text Document.txt', 'r').read()
OD = pd.read_csv('OD_set_auto.csv')
gmaps = googlemaps.Client(k)

OD['origin'] = [[OD['ox'][x], OD['oy'][x]] for x in range(OD.shape[0])]
OD['dest'] = [[OD['dx'][x], OD['dy'][x]] for x in range(OD.shape[0])]

OD_test = OD.iloc[:15]

t_model = ['pessimistic', 'optimistic', 'best_guess']

OD_test['Traffic_model'] = np.nan
pd_list = list()
for d, f in enumerate(t_model):
    g = OD_test[:]
    g['Traffic_model'].fillna(f, inplace=True)
    pd_list.append(g)


OD_test = pd.concat(pd_list).reset_index()


DT = datetime.strptime('2018-10-3 07:00', '%Y-%m-%d %H:%M')

direct = gmaps.directions(origin=OD_test['origin'],
                          destination=OD_test['dest'][1],
                          mode='driving',
                          alternatives=True,
                          traffic_model=OD_test['Traffic_model'][1],
                          departure_time=DT)

direct[1]['legs'][0]['steps'][5]['html_instructions']

direct[1]['legs'][0]['duration_in_traffic']
direct[0]['legs'][0]['steps'][2]['html_instructions']
direct[0]['legs'][0]['steps'][1].keys()
direct[0]['summary']

results = []
for i in range(0,130,10):
    slc = OD_test.iloc[i:i+10]

    for x in range(slc.shape[0]):
        direct = gmaps.directions(origin=slc['origin'][x], destination=slc['dest'][x], mode='driving',
                              alternatives=True,
                              departure_time=DT,
                              traffic_model=slc['Traffic_model'][x])
    results.append(direct)

cPickle.dump(results, open('results.p', 'wb'))
# results = cPickle.load(open('results.p', 'rb'))

results[0][1]['legs'][0].keys()
results[0][0]['legs'][0]['steps'][1]['html_instructions']
results[0][0]['legs'][0]['steps'][1]['duration']['text']
results[1][0]['legs'][0]['departure_time']


summary = []
for idx, val in enumerate(results):
    if val == []:
        x = []
    else:
        x = val
        OD_sum = []
        for index, value in enumerate(x):
            y = value['summary']
            OD_sum.append(y)
    summary.append(OD_sum)

res = []
for idx, val in enumerate(results):
    if val == []:
        x = []
    else:
        x = val
        OD_legs = []
        for index, value in enumerate(x):
            y = value['legs']
            OD_legs.append(y)
    res.append(OD_legs)

distance = []
duration = []
duration_in_traffic = []
for idx, val in enumerate(res):
    if val == []:
        r = []
    else:
        r = val
        dist_list = []
        dur_list = []
        dur_t_list = []
        for index, value in enumerate(r):
            dist = value[0]['distance']['value']
            dist_list.append(dist)
            dur = value[0]['duration']['value']
            dur_list.append(dur)
            dur_t = value[0]['duration_in_traffic']['value']
            dur_t_list.append(dur_t)
    distance.append(dist_list)
    duration.append(dur_list)
    duration_in_traffic.append(dur_t_list)

step = []
for idx, val in enumerate(res):
    if val == []:
        r = []
    else:
        r = val
        step_list = []
        for index, value in enumerate(r):
            s = value[0]['steps']
            step_list.append(s)
    step.append(step_list)

step_dist = []
step_duration = []
step_end_loc = []
step_start_loc = []
step_html = []
for idx, val in enumerate(step):
    if val == []:
        u = []
    else:
        u = val
        u_dir = []
        u_dur = []
        u_end = []
        u_str = []
        u_html = []
        for y in u:
            st = y
            dist_list = []
            dur_list = []
            end_loc_list = []
            str_loc_list = []
            html_list = []
            for index, value in enumerate(st):
                dist = value['distance']['value']
                dist_list.append(dist)
                dur = value['duration']['value']
                dur_list.append(dur)
                end_loc = value['end_location']
                end_loc_list.append(end_loc)
                str_loc = value['start_location']
                str_loc_list.append(str_loc)
                dir = value['html_instructions']
                html_list.append(dir)
            u_dir.append(dist_list)
            u_dur.append(dur_list)
            u_end.append(end_loc_list)
            u_str.append(str_loc_list)
            u_html.append(html_list)
    step_dist.append(u_dir)
    step_duration.append(u_dur)
    step_end_loc.append(u_end)
    step_start_loc.append(u_str)
    step_html.append(u_html)

initial_col_list = list(OD_test.columns)

OD_test['Summary'] = [summary[x] for x in range(OD_test.shape[0])]
OD_test['Distance'] = [distance[x] for x in range(OD_test.shape[0])]
OD_test['Durations_sec'] = [duration[x] for x in range(OD_test.shape[0])]
OD_test['duration_in_traffic'] = [duration_in_traffic[x] for x in range(OD_test.shape[0])]
OD_test['Step_dist'] = [step_dist[x] for x in range(OD_test.shape[0])]
OD_test['step_duration'] = [step_duration[x] for x in range(OD_test.shape[0])]
OD_test['step_end_loc'] = [step_end_loc[x] for x in range(OD_test.shape[0])]
OD_test['step_start_loc'] = [step_start_loc[x] for x in range(OD_test.shape[0])]
OD_test['step_html'] = [step_html[x] for x in range(OD_test.shape[0])]

col_list = list(OD_test.columns[14:23])

cols = dict()
for n in col_list:
    s = OD_test.apply(lambda x: pd.Series(x[n]), axis=1).stack().reset_index(level=1, drop=True)
    s.name = n
    # s = s.reset_index()
    cols[n] = s

o = pd.DataFrame.from_records(cols)

OD_test = pd.merge(OD_test[initial_col_list], o, left_index=True, right_index=True)

OD_test = OD_test.reset_index()

col_list = list(OD_test.columns[15:25])
cols = dict()
for n in col_list:
    s = OD_test.apply(lambda x: pd.Series(x[n]), axis=1).stack().reset_index(level=1, drop=True)
    s.name = n
    # s = s.reset_index()
    cols[n] = s

p = pd.DataFrame.from_records(cols)

OD_test = pd.merge(OD_test[initial_col_list], p, left_index=True, right_index=True)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


OD_test['step_html'] = OD_test['step_html'].apply(cleanhtml)

OD_test.to_csv('test.csv')
