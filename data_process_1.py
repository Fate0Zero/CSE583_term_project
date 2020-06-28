import pandas as pd
import numpy as np
import seaborn as sns
import csv
import pandas.util.testing as tm


champs = pd.read_csv('./data/champs.csv')
matches = pd.read_csv('./data/matches.csv')
participants = pd.read_csv('./data/participants.csv')
stats1 = pd.read_csv('./data/stats1.csv')
stats2 = pd.read_csv('./data/stats2.csv')
stats = stats1.append(stats2)


df = pd.merge(participants, stats, how = 'left', on = ['id'], suffixes=('', '_y'))
df = pd.merge(df, champs, how = 'left', left_on = 'championid', right_on = 'id', suffixes=('', '_y'))
df = pd.merge(df, matches, how = 'left', left_on = 'matchid', right_on = 'id', suffixes=('', '_y'))

def final_position(row):
    if row['role'] in ('DUO_SUPPORT', 'DUO_CARRY'):
        return row['role']
    else:
        return row['position']

df['adjposition'] = df.apply(final_position, axis = 1) 

df['team'] = df['player'].apply(lambda x: '1' if x <= 5 else '2')
df['team_role'] = df['team'] + ' - ' + df['adjposition']

# remove matchid with duplicate roles, e.g. 3 MID in same team, etc
remove_index = []
for i in ('1 - MID', '1 - TOP', '1 - DUO_SUPPORT', '1 - DUO_CARRY', '1 - JUNGLE', '2 - MID', '2 - TOP', '2 - DUO_SUPPORT', '2 - DUO_CARRY', '2 - JUNGLE'):
    df_remove = df[df['team_role'] == i].groupby('matchid').agg({'team_role':'count'})
    remove_index.extend(df_remove[df_remove['team_role']!=1].index.values)

# remove the matchid with player less than 10
df_remove = df.groupby('matchid').agg({'player':'count'})
remove = df_remove['player'] < 10
df_remove = df_remove[remove]
remove_index.extend(df_remove.index.values)

# remove unclassified BOT, correct ones should be DUO_SUPPORT OR DUO_CARRY
remove_index.extend(df[df['adjposition'] == 'BOT']['matchid'].unique())
remove_index = list(set(remove_index))

print('# matches in dataset before cleaning: {}'.format(df['matchid'].nunique()))
df = df[~df['matchid'].isin(remove_index)]
print('# matches in dataset after cleaning: {}'.format(df['matchid'].nunique()))

# df = df[['id', 'matchid', 'player', 'name', 'adjposition', 'team_role', 'win', 'kills', 'deaths', 'assists', 'turretkills','totdmgtochamp', 'totheal', \
#     'totminionskilled', 'goldspent', 'totdmgtaken', 'inhibkills', 'pinksbought', 'wardsplaced', 'duration', 'platformid', 'seasonid', 'version']]

df = df[['id', 'matchid', 'player', 'name', 'adjposition', 'team_role', 'win', 'kills', 'deaths', 'assists', 'seasonid', 'version']]

df_2 = df.sort_values(['matchid','adjposition'], ascending = [1,1])
df_2['shift 1'] = df_2['name'].shift()
df_2['shift -1'] = df_2['name'].shift(-1)

def get_matchup(x):
    if x['player'] <= 5: #team 1
        if x['name'] < x['shift -1']:
            name_return = x['name'] + ' vs ' + x['shift -1']
        else:
            name_return = x['shift -1'] + ' vs ' + x['name']
    else:  # team 2
        if x['name'] < x['shift 1']:
            name_return = x['name'] + ' vs ' + x['shift 1']
        else:
            name_return = x['shift 1'] + ' vs ' + x['name']
    return name_return

def opponent(x):
    if x['name'] == x['match up'].split(' vs')[0]:
        opponent_name = x['match up'].split(' vs')[1] 
    else:  
        opponent_name = x['match up'].split(' vs')[0] 
    return opponent_name

df_2['match up'] = df_2.apply(get_matchup, axis = 1)
df_2['win_adj'] = df_2.apply(lambda x: x['win'] if x['name'] == x['match up'].split(' vs')[0] else 0, axis = 1)
df_2['opponent_name'] = df_2.apply(opponent, axis = 1)


# calculate dominant score
df_matchup = df_2.groupby(['adjposition', 'match up']).agg({'win_adj': 'sum', 'match up': 'count'})
df_matchup.columns = ['win matches', 'total matches']
df_matchup['total matches'] = df_matchup['total matches'] / 2
df_matchup['win rate'] = df_matchup['win matches'] /  df_matchup['total matches']  * 100
df_matchup['dominant score'] = df_matchup['win rate'] - 50
df_matchup['dominant score (ND)'] = abs(df_matchup['dominant score'])


df_matchup = df_matchup.sort_values('dominant score (ND)', ascending = False)
df_matchup = df_matchup[['total matches', 'dominant score']]                   
df_matchup = df_matchup.reset_index()


df_temp = df_2.merge(df_matchup, how = 'left', left_on = ['match up', 'adjposition'], right_on = ['match up', 'adjposition'], suffixes=('_1', '_2'))
df_temp = df_temp[['matchid', 'player', 'name', 'opponent_name', 'match up', 'adjposition', 'team_role', 'dominant score', 'win', 'kills', 'deaths', 'assists', 'seasonid']]

# win rate
pd.options.display.float_format = '{:,.1f}'.format
df_win_rate_role = df.groupby(['name','adjposition']).agg({'win': 'sum', 'name': 'count', 'kills': 'mean', 'deaths': 'mean', 'assists': 'mean'})
df_win_rate_role.columns = ['win matches', 'total matches', 'K', 'D', 'A']
df_win_rate_role['win rate'] = df_win_rate_role['win matches'] /  df_win_rate_role['total matches'] * 100
df_win_rate_role['KDA'] = (df_win_rate_role['K'] + df_win_rate_role['A']) / df_win_rate_role['D']
df_win_rate_role = df_win_rate_role.sort_values('win rate', ascending = False)
df_win_rate_role = df_win_rate_role[['total matches', 'win rate', 'K', 'D', 'A', 'KDA']]
df_win_rate_role = df_win_rate_role.reset_index()

df_final = df_temp.merge(df_win_rate_role, how = 'left', left_on = ['name','adjposition'], right_on = ['name','adjposition'], suffixes=('_1', '_2'))

df_final = df_final[['matchid', 'player', 'name', 'opponent_name', 'match up', 'adjposition', 'team_role', 'dominant score', 'win', 'win rate', 'kills', 'deaths', 'assists', 'seasonid', 'K', 'D', 'A', 'KDA', 'total matches']]


df_final.to_csv('data_process_1.csv')
