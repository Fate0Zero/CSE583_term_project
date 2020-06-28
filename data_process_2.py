import pandas as pd
import numpy as np
import seaborn as sns
import pandas.util.testing as tm
import csv

count = 1
big_list = []
temp_list = []
prev_match = 0
curr_match = 0
with open('./data_process_1.csv') as csvfile:
    next(csvfile)
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        curr_match = row[1]
        if count == 1:
            prev_match = curr_match   
        if curr_match == prev_match:
            temp_list.append(row)
            prev_match = curr_match
            count = count + 1
        else:
            count = 2
            temp_list = []
            temp_list.append(row)
            prev_match = curr_match
        if count == 11:
            count = 1
            for x in temp_list:
                big_list.append(x)
            temp_list = []
            prev_match = 0
            curr_match = 0

df = pd.DataFrame(big_list)

df.columns = ['id', 'matchid', 'player', 'name', 'opponent_name', 'match_up', 'adjposition', 'team_role', 'dominant_score', 'win', 'win rate', 'kills', 'deaths', 'assists', 'seasonid', 'K', 'D', 'A', 'KDA', 'total matches']
df = df[['matchid', 'player', 'name', 'opponent_name', 'match_up', 'adjposition', 'team_role', 'dominant_score', 'win', 'win rate', 'kills', 'deaths', 'assists', 'seasonid', 'K', 'D', 'A', 'KDA', 'total matches']]
df.to_csv('data_process_2.csv')
