import pandas as pd

# Read the CSV file
df = pd.read_csv("Oceania_covid_data.csv")

# Define the threshold for high-risk days
threshold = 2000

# Function to check if a day is high risk
def is_high_risk(index):
    if index < 14:
        return False
    sum_cases = df.loc[index-14:index, 'cases'].sum()
    return sum_cases >= threshold

# Create a new column 'high_risk_2k' based on the sum of cases for the last 15 days
df['high_risk_2k'] = [is_high_risk(index) for index in range(len(df))]

# Save the modified DataFrame to a new CSV file
df.to_csv("Oceania_covid_data.csv", index=False)
