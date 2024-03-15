from rdflib import Graph, Namespace
import re
import csv
from datetime import datetime

def extract_variables():
    # Load the RDF file
    g = Graph()
    g.parse("/home/rodrirocki/Thesis/ontologies/covid.rdf")

    # Define the namespace
    covid = Namespace("http://www.semanticweb.org/rodrigo/ontologies/2024/1/covid/")

    # Initialize a list to store the extracted variables
    extracted_variables = []

    # Iterate over the triples to find the DASE_RULE section
    for subj, _, obj in g.triples((None, covid["DASE_RULE"], None)):
        # Extract the rule from the DASE_RULE section
        if obj.startswith("Mapping"):
            # Use regex to extract the variables
            match1 = re.findall(r"___(\w+)\([^)]*\)", obj)
            match2 = re.findall(r"-> (\w+)\(",obj)
            
            # Append the extracted variables to the list
            if match1 and match2:
                extracted_variables.append(match1[0])
                extracted_variables.append(match2[0])
    return extracted_variables



def is_date(string):
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"] #Add more formats if needed
    for fmt in formats:
        try:
            datetime.strptime(string, fmt)
            return True
        except ValueError:
            pass
    return False



def apply_rules_to_value(value, extracted_variables):
    result = {}
    if is_date(value):
        if(extracted_variables[1] == 'Season'):
            date = datetime.strptime(value, "%d/%m/%Y")
            month = date.month
            day = date.day
            if (month == 3 and day >= 20) or (month == 4 or month == 5) or (month == 6 and day < 21):
                result[extracted_variables[1]] = "Spring"
                return result
            elif (month == 6 and day >= 21) or (month == 7 or month == 8) or (month == 9 and day < 23):
                result[extracted_variables[1]] = "Summer"
                return result
            elif (month == 9 and day >= 23) or (month == 10 or month == 11) or (month == 12 and day < 21):
                result[extracted_variables[1]] = "Autumn"
                return result
            else:
                result[extracted_variables[1]] = "Winter"
                return result
        #add more cases if needed
    #add more cases if needed
        


def process_csv(csv_file,extracted_variables):
    updated_rows = []
    
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Iterate over each row
        for row in reader:
            # Apply rules to the specified variable in the row
            new_variables = apply_rules_to_value(row[extracted_variables[0]], extracted_variables)
            # Update the row with new variables
            row.update(new_variables)
            
            # Append the updated row to the list
            updated_rows.append(row)
    
    # Write the updated dataset back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        fieldnames = updated_rows[0].keys() if updated_rows else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the updated rows
        writer.writerows(updated_rows)


if __name__ == "__main__":
    rdf_file = "/home/rodrirocki/Thesis/ontologies/covid.rdf"  # Replace with the path to your RDF file
    csv_file = "/home/rodrirocki/Thesis/case_study/Oceania_covid_data.csv"  # Replace with the path to your CSV file
    extracted_variables = extract_variables()
    process_csv(csv_file, extracted_variables)
