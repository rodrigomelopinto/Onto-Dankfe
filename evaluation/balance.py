#%%
from pandas import read_csv, concat, DataFrame, Series
from matplotlib.pyplot import figure, savefig, show
from ds_charts import bar_chart, multiple_bar_chart
from imblearn.over_sampling import SMOTE

file = "covid_oceania"
filename = '/home/rodrirocki/Thesis/evaluation/data/covid_oceania_cleaned.csv'
original = read_csv(filename, sep=',', decimal='.')
class_var = 'high_risk_2k'
target_count = original[class_var].value_counts()
positive_class = target_count.idxmin()
negative_class = target_count.idxmax()
#ind_positive_class = target_count.index.get_loc(positive_class)
print('Minority class=', positive_class, ':', target_count[positive_class])
print('Majority class=', negative_class, ':', target_count[negative_class])
print('Proportion:', round(target_count[positive_class] / target_count[negative_class], 2), ': 1')
values = {'Original': [target_count[positive_class], target_count[negative_class]]}

figure()
bar_chart(target_count.index, target_count.values, title='Class balance')
savefig(f'images/{file}_balance.png')

df_positives = original[original[class_var] == positive_class]
df_negatives = original[original[class_var] == negative_class]


df_neg_sample = DataFrame(df_negatives.sample(len(df_positives)))
df_under = concat([df_positives, df_neg_sample], axis=0)
df_under.to_csv(f'data/{file}_under.csv', index=False)
values['UnderSample'] = [len(df_positives), len(df_neg_sample)]
print('Minority class=', positive_class, ':', len(df_positives))
print('Majority class=', negative_class, ':', len(df_neg_sample))
print('Proportion:', round(len(df_positives) / len(df_neg_sample), 2), ': 1')

df_pos_sample = DataFrame(df_positives.sample(len(df_negatives), replace=True))
df_over = concat([df_pos_sample, df_negatives], axis=0)
df_over.to_csv(f'data/{file}_over.csv', index=False)
values['OverSample'] = [len(df_pos_sample), len(df_negatives)]
print('Minority class=', positive_class, ':', len(df_pos_sample))
print('Majority class=', negative_class, ':', len(df_negatives))
print('Proportion:', round(len(df_pos_sample) / len(df_negatives), 2), ': 1')

# %%