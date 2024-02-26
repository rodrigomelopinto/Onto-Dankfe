import pandas as pd

# Read the CSV file
df = pd.read_csv("GlobalLandTemperatures_GlobalLandTemperaturesByMajorCity.csv")

# Calculate yearly average temperature for each city
df['year'] = df['dt'].str.slice(0, 4)
df['yearly_avg_temp'] = df.groupby(['City', 'year'])['AverageTemperature'].transform('mean')

# Create the 'average_diff_pos' column based on whether daily temperature is above yearly average
df['average_diff_pos'] = df['AverageTemperature'] > df['yearly_avg_temp']

df.drop(columns=['year', 'yearly_avg_temp'], inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv("GlobalLandTemperatures_GlobalLandTemperaturesByMajorCity.csv", index=False)