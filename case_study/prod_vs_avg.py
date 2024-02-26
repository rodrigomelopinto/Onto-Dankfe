import pandas as pd

# Read the CSV file
df = pd.read_csv("gridwatch.csv")

# Function to extract hour from timestamp string
def extract_hour(timestamp):
    return int(timestamp.split()[1].split(':')[0])

# Calculate the sum of energy production for each instance
df['total_energy'] = df[' coal'] + df[' nuclear'] + df[' ccgt'] + df[' wind'] + df[' pumped'] + df[' solar'] + df[' hydro'] + df[' biomass']

# Group by hour and calculate the hourly average energy production
hourly_avg_energy = df.groupby(df[' timestamp'].apply(extract_hour))['total_energy'].mean()

# Function to determine if energy production is above the hourly average
def is_prod_above_avg(row):
    hour = extract_hour(row[' timestamp'])
    avg_energy = hourly_avg_energy[hour]
    return row['total_energy'] > avg_energy

# Create the 'prod_vs_avg' column based on whether energy production is above the hourly average
df['prod_vs_avg'] = df.apply(is_prod_above_avg, axis=1)

df.drop(columns=['total_energy'], inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv("gridwatch.csv", index=False)
