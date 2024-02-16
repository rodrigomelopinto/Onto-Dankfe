import pandas as pd

# Load your COVID dataset into a pandas DataFrame
covid_data = pd.read_csv("data.csv")

# Iterate over unique continent values
for continent in covid_data['continentExp'].unique():
    # Filter the DataFrame for each continent
    continent_data = covid_data[covid_data['continentExp'] == continent]
    
    # Save each filtered DataFrame as a separate dataset
    filename = f"{continent}_covid_data.csv"
    continent_data.to_csv(filename, index=False)
