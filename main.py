import numpy as np
import csv
import pandas as pd
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import statistics 

df = pd.read_csv('./final_data.csv')
df = df.astype(float)
df.dropna(inplace=True)

y = df.iloc[0:, 0:1]
x = df.iloc[0:, 2:]

#pca = PCA(n_components="mle")
#x = pca.fit_transform(x)

# lda = LinearDiscriminantAnalysis()
# lda.fit(x_train,y_train.values.ravel())
# x = lda.transform(x)
train_list = []
test_list = []
for i in range(0, 100):
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.6)

    clf = LogisticRegression(penalty='l2') 
    clf.fit(x_train, y_train.values.ravel())

    y_hat_1 = clf.predict(x_train)
    y_hat_2 = clf.predict(x_test)

    train_list.append(accuracy_score(y_train.values.ravel(), y_hat_1).item())
    test_list.append(accuracy_score(y_test.values.ravel(), y_hat_2).item())
    print(i)


print("train mean:")
print(statistics.mean(train_list))
print("train std:")
print(statistics.stdev(train_list))

print("test mean:")
print(statistics.mean(test_list))
print("test std:")
print(statistics.stdev(test_list))


# y_train = y_train.values.ravel()
# y_test = y_test.values.ravel()

# P = 0
# TP = 0
# N = 0
# FP = 0
# TN = 0
# for x, y in zip(y_test, y_hat_2):
#     if x == 0:
#         P = P + 1
#         if y == 0:
#             TP = TP + 1
#     else:
#         N = N + 1
#         if y == 0:
#             FP = FP + 1
#         if y == 1:
#             TN = TN + 1

# TPR = TP/P
# FPR = FP/N
# accuracy = (TP+TN)/(N+P)