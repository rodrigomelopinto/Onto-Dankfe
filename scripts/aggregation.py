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
    extracted_variables = {}
    variables = []

    # Iterate over the triples to find the DASE_RULE section
    for subj, _, obj in g.triples((None, covid["DASE_RULE"], None)):
        # Extract the rule from the DASE_RULE section
        if obj.startswith("Aggregation"):
            # Use regex to extract the variables
            match1 = re.findall(r"___(\w+)\([^)]*\)", obj)
            match2 = re.findall(r'\^ (\w+)\(', obj)
            match3 = re.findall(r"-> (\w+)\(",obj)
            
            # Append the extracted variables to the list
            if match1 and match2 and match3:
                variables.append(match1[0])
                for n in range(len(match2)):
                    variables.append(match2[n])
                extracted_variables[match3[0]] = variables
            for n in range(len(extracted_variables[match3[0]])):
                if extracted_variables[match3[0]][n] == 'sum':
                    tmp = extracted_variables[match3[0]][n]
                    aux = extracted_variables[match3[0]][0]
                    extracted_variables[match3[0]].remove(aux)
                    extracted_variables[match3[0]].remove(tmp)
                    extracted_variables[match3[0]].insert(0,tmp)
                    extracted_variables[match3[0]].insert(1,aux)
                #add more cases for different operation like stdev etc
    return extracted_variables



def apply_rules_to_value(value, new_variable):
    result = []
    
        #add more cases if needed
    #add more cases if needed
        


def process_csv(csv_file,extracted_variables):
    updated_rows = []
    new_variables = {}

    for var in extracted_variables:
        if extracted_variables[var][0] == 'sum':
            aggregated_values = {}

            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    group_value = row[extracted_variables[var][2]]

                    if group_value not in aggregated_values:
                        aggregated_values[group_value] = {extracted_variables[var][1] : 0}

                    aggregated_values[group_value][extracted_variables[var][1]] += int(row[extracted_variables[var][1]])
            
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    group_value = row[extracted_variables[var][2]]
                    new_variables[var] = aggregated_values[group_value][extracted_variables[var][1]]

                    row.update(new_variables)
                    updated_rows.append(row)
    
            # Write the updated dataset back to the CSV file
            with open(csv_file, 'w', newline='') as file:
                fieldnames = updated_rows[0].keys() if updated_rows else []
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Write the header
                writer.writeheader()
                
                # Write the updated rows
                writer.writerows(updated_rows)
        #add more cases to the other operations like stdev


if __name__ == "__main__":
    rdf_file = "/home/rodrirocki/Thesis/ontologies/covid.rdf"  # Replace with the path to your RDF file
    csv_file = "/home/rodrirocki/Thesis/case_study/Oceania_covid_data.csv"  # Replace with the path to your CSV file
    extracted_variables = extract_variables()
    process_csv(csv_file, extracted_variables)