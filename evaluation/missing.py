#%%
from pandas import read_csv
from pandas.plotting import register_matplotlib_converters
from matplotlib.pyplot import figure, savefig, show
from ds_charts import bar_chart, get_variable_types
from sklearn.impute import SimpleImputer
from pandas import concat, DataFrame
from numpy import nan


register_matplotlib_converters()
file = 'diabetic_data'
filename = '../diabetic_data.csv'
data = read_csv(filename, na_values='?')

#1st approach
data = data.drop(['weight'],axis=1)
data = data.drop(['payer_code'],axis=1)
data['medical_specialty'] = data['medical_specialty'].fillna('Missing')
data['race'] = data['race'].fillna('Missing')
data = data.fillna('Missing')
data.to_csv(f'data/{file}_mv_constant.csv', index=True)

#2st approach
# data = data.drop(['weight'],axis=1)
# data = data.drop(['payer_code'],axis=1)

tmp_nr, tmp_sb, tmp_bool = None, None, None
variables = get_variable_types(data)
numeric_vars = variables['Numeric']
symbolic_vars = variables['Symbolic']
binary_vars = variables['Binary']

tmp_nr, tmp_sb, tmp_bool = None, None, None
if len(numeric_vars) > 0:
    imp = SimpleImputer(strategy='mean', missing_values=nan, copy=True)
    tmp_nr = DataFrame(imp.fit_transform(data[numeric_vars]), columns=numeric_vars)
if len(symbolic_vars) > 0:
    imp = SimpleImputer(strategy='most_frequent', missing_values=nan, copy=True)
    tmp_sb = DataFrame(imp.fit_transform(data[symbolic_vars]), columns=symbolic_vars)
if len(binary_vars) > 0:
    imp = SimpleImputer(strategy='most_frequent', missing_values=nan, copy=True)
    tmp_bool = DataFrame(imp.fit_transform(data[binary_vars]), columns=binary_vars)

df = concat([tmp_nr, tmp_sb, tmp_bool], axis=1)
df.index = data.index
df.to_csv(f'data/{file}_mv_most_frequent.csv', index=True)
# %%