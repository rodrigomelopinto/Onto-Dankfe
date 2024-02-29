#%%
import pandas as pd
from matplotlib.pyplot import figure, savefig, show
from ds_charts import bar_chart, get_variable_types
from pandas import DataFrame


file = 'covid_oceania'
data = pd.read_csv("/home/rodrirocki/Thesis/case_study/Oceania_covid_data.csv", na_values='', parse_dates=True, infer_datetime_format=True)
#data['dateRep'] = pd.to_datetime(data['dateRep'],format = '%d/%m/%Y')

pd.plotting.register_matplotlib_converters()

data.shape

variable_types = get_variable_types(data)
counts = {}
for tp in variable_types.keys():
    counts[tp] = len(variable_types[tp])
figure(figsize=(4,2))
bar_chart(list(counts.keys()), list(counts.values()), title='Nr of variables per type')
savefig('images/variable_types.png')

data.dropna(inplace=True)

mv = {}
for var in data:
    nr = data[var].isna().sum()
    if nr > 0:
        mv[var] = nr
print(mv)
data.to_csv(f'data/{file}_cleaned.csv', index=True)

'''figure(figsize=(4,2))
bar_chart(list(mv.keys()), list(mv.values()), title='Nr of missing values per variable',
            xlabel='variables', ylabel='nr missing values', rotation=True)
savefig('images/mv.png')'''
# %%