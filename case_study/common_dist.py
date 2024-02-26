import pandas as pd

# Read the CSV file
df = pd.read_csv("BPD_Part_1_Victim_Based_Crime_Data.csv")

# Define the threshold for determining a common crime code in a district
threshold = 100  # You can adjust this threshold as needed

# Group the DataFrame by 'CrimeCode' and 'District' and count the number of occurrences
crime_district_counts = df.groupby(['CrimeCode', 'District']).size()

# Create a set of (Crime Code, District) pairs where the count exceeds the threshold
common_crime_district_pairs = set(crime_district_counts[crime_district_counts >= threshold].index)

# Function to determine if a crime code is common in a specific district
def is_common_crime_code_in_district(row):
    crime_code = row['CrimeCode']
    district = row['District']
    return (crime_code, district) in common_crime_district_pairs

# Create the 'common_dist' column based on whether the crime code is common in the district
df['common_dist'] = df.apply(is_common_crime_code_in_district, axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv("BPD_Part_1_Victim_Based_Crime_Data.csv", index=False)
