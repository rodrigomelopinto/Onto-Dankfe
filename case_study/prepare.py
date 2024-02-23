import pandas as pd

# Load your COVID dataset into a pandas DataFrame
covid_data = pd.read_csv("Oceania_covid_data.csv")
covid_data.drop(columns=['cases_per_100k'], inplace=True)
covid_data.to_csv("Oceania_covid_data.csv", index=False)
