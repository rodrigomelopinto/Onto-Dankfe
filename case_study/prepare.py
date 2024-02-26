import pandas as pd

# Load your COVID dataset into a pandas DataFrame
covid_data = pd.read_csv("gridwatch.csv")
covid_data.drop(columns=['prod_vs_avg'], inplace=True)
covid_data.to_csv("gridwatch.csv", index=False)
