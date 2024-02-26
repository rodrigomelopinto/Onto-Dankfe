import pandas as pd

# Read the CSV file
df = pd.read_csv("gridwatch.csv")

# Calculate the hourly average energy production
hourly_avg_production = df.iloc[:, 4:].mean(axis=1).groupby(df.index // 12).transform('mean')

# Function to determine if energy production is above hourly average
def is_prod_above_avg(row):
    index = row.name
    hour_group = index // 12
    total_production = row.iloc[4:].sum()  # Calculate total production for this instance
    print(total_production > hourly_avg_production[hour_group])
    return total_production > hourly_avg_production[hour_group]

# Create the 'prod_vs_avg' column based on whether energy production is above hourly average
df['prod_vs_avg'] = df.apply(is_prod_above_avg, axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv("gridwatch.csv", index=False)
