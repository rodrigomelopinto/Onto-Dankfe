#%%
from pandas import read_csv, concat, DataFrame, Series
from matplotlib.pyplot import figure, savefig, show
from ds_charts import bar_chart, multiple_bar_chart
from imblearn.over_sampling import SMOTE

file = "diabetic"
filename = 'dataWeek3/diabetic_scaled_zscore.csv'
original = read_csv(filename, sep=',', decimal='.')
class_var = 'readmitted'
target_count = original[class_var].value_counts()
u30_class = target_count.idxmin()
a30_class = '>30'
negative_class = target_count.idxmax()
#print(a30_class)

#ind_positive_class = target_count.index.get_loc(positive_class)
print('Minority class=',u30_class, ':', target_count[u30_class])
print('Middle class=',a30_class, ':', target_count[a30_class])
print('Majority class=', negative_class, ':', target_count[negative_class])
print('Proportion:', round(target_count[u30_class] / target_count[negative_class], 2), ': 1')
values = {'Original': [target_count[u30_class],target_count[a30_class], target_count[negative_class]]}

figure()
bar_chart(target_count.index, target_count.values, title='Class balance')
savefig(f'imagesWeek3/{file}_balance.png')
show()

df_u30 = original[original[class_var] == u30_class]
df_a30 = original[original[class_var] == a30_class]
df_negatives = original[original[class_var] == negative_class]


df_neg_sample = DataFrame(df_negatives.sample(len(df_u30)))
df_a30_sample = DataFrame(df_a30.sample(len(df_u30)))
df_under = concat([df_u30, df_a30_sample, df_neg_sample], axis=0)
df_under.to_csv(f'dataWeek3/{file}_under.csv', index=False)
values['UnderSample'] = [len(df_u30), len(df_a30_sample), len(df_neg_sample)]
print('Minority class=', u30_class, ':', len(df_u30))
print('Middle class=', a30_class, ':', len(df_a30_sample))
print('Majority class=', negative_class, ':', len(df_neg_sample))
print('Proportion:', round(len(df_u30) / len(df_neg_sample), 2), ': 1')

df_u30_sample = DataFrame(df_u30.sample(len(df_negatives), replace=True))
df_a30_sample = DataFrame(df_a30.sample(len(df_negatives), replace=True))
df_over = concat([df_u30_sample, df_a30_sample, df_negatives], axis=0)
df_over.to_csv(f'dataWeek3/{file}_over.csv', index=False)
values['OverSample'] = [len(df_u30_sample), len(df_a30_sample), len(df_negatives)]
print('Minority class=', u30_class, ':', len(df_u30_sample))
print('Middle class=', a30_class, ':', len(df_a30_sample))
print('Majority class=', negative_class, ':', len(df_negatives))
print('Proportion:', round(len(df_u30_sample) / len(df_negatives), 2), ': 1')

RANDOM_STATE = 42

smote = SMOTE(sampling_strategy='not majority', random_state=RANDOM_STATE)
y = original.pop(class_var).values
X = original.values
smote_X, smote_y = smote.fit_resample(X, y)

df_smote = concat([DataFrame(smote_X), DataFrame(smote_y)], axis=1)
df_smote.columns = list(original.columns) + [class_var]
df_smote.to_csv(f'dataWeek3/{file}_smote.csv', index=False)

smote_target_count = Series(smote_y).value_counts()
values['SMOTE'] = [smote_target_count[u30_class], smote_target_count[a30_class], smote_target_count[negative_class]]
print('Minority class=', u30_class, ':', smote_target_count[u30_class])
print('Middle class=', a30_class, ':', smote_target_count[a30_class])
print('Majority class=', negative_class, ':', smote_target_count[negative_class])
print('Proportion:', round(smote_target_count[u30_class] / smote_target_count[negative_class], 2), ': 1')

figure()
multiple_bar_chart([u30_class, a30_class, negative_class], values, title='Target', xlabel='frequency', ylabel='Class balance')
show()
# %%