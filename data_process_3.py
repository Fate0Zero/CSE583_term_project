import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas.util.testing as tm
import csv
import matplotlib.pyplot as plt

big_list = []
temp_list = []
count = 0
with open('./data_process_2.csv') as csvfile:
    next(csvfile)
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        if count == 0:
            if int(float(row[9])) == 0:         # if team 1 win, then win = 0, if team 2 win, then win = 1
                temp_list.append('0')
            else:
                temp_list.append('1')
            #temp_list.append(row[1]) #matchid
            temp_list.append(row[14]) #seasonid

        # dominant scores
        if count % 2 == 0:
            if row[5].split(' vs ')[0] == row[3]:
                temp_list.append(row[8])
            else:
                temp_list.append(str(-float(row[8])))

        temp_list.append(row[10]) #win rate
        temp_list.append(row[15]) #K
        temp_list.append(row[16]) #D
        temp_list.append(row[17]) #A
        temp_list.append(row[18]) # average KDA
        temp_list.append(row[19]) # total matches
  
        count = count + 1
        if count == 10:
            big_list.append(temp_list)
            temp_list = []
            count = 0

df = pd.DataFrame(big_list)

df.to_csv('final_data.csv', index=False)


# y = df.iloc[0:, 0:1]
# y = y.values.ravel()
# unique, counts = np.unique(y, return_counts=True)
# print(unique)
# print(counts)
# barlist = plt.bar(unique, counts)
# barlist[0].set_color('r')
# barlist[1].set_color('b')
# plt.title('Class Frequency of two classes')
# plt.xlabel('Class')
# plt.ylabel('Frequency')
# plt.show()

# y = df.iloc[0:, 0:1]
# y = y.values.ravel()
# unique, counts = np.unique(y, return_counts=True)
# print(unique)
# print(counts)