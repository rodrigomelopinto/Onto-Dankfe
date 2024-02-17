import re
import csv
from rdflib import Graph, Namespace

def extract_variables(rule):
    """
    Extract variables from the rule string.
    """
    # Match variables in the rule string
    variables = re.findall(r'\?\w+', rule)
    return variables

def apply_rule(rule, variables_dict):
    """
    Apply the rule to generate new variables.
    """
    # Extract variables from the rule
    variables = extract_variables(rule)
    
    # Apply transformations
    new_variables = []
    for var in variables:
        if var in variables_dict:
            new_var = variables_dict[var]
            new_variables.append(new_var)
        else:
            new_variables.append(var)  # Keep unchanged if not found in variables_dict
            
    return new_variables

def process_rules(rules):
    """
    Process rules and generate variables.
    """
    # Initialize variables dictionary
    variables_dict = {}
    
    # Process each rule
    for rule in rules:
        new_variables = apply_rule(rule, variables_dict)
        
        # Update variables dictionary with new variables
        for i, var in enumerate(new_variables):
            if var.startswith('?') and var not in variables_dict:
                variables_dict[var] = f'new_var_{len(variables_dict)}'  # Generate new variable name
                
    return variables_dict

def read_rules_from_rdf(rdf_file):
    """
    Read rules from RDF file.
    """
    # Create an RDF graph
    g = Graph()

    # Parse the RDF file
    g.parse(rdf_file)

    # Define namespaces
    covid = Namespace("http://www.semanticweb.org/rodrigo/ontologies/2024/1/covid/")
    
    # Initialize rules list
    rules = []

    # Find triples with DASE_RULE property
    for subj, _, obj in g.triples((None, covid["DASE_RULE"], None)):
        rules.append(obj)
    
    return rules

def apply_rules_to_value(rules, value, variable_to_update):
    """
    Apply rules to the given value to generate new variables.
    """
    # Initialize variables dictionary
    variables_dict = {variable_to_update: value}
    
    # Apply rules to generate new variables
    for rule in rules:
        new_variables = apply_rule(rule, variables_dict)
        
        
        # Update variables dictionary with new variables
        for i, var in enumerate(new_variables):
            if var.startswith('?') and var not in variables_dict:
                if var == '?day':
                    # Extract the day part from the current_date value
                    day_part = value.split('/')[0]
                    variables_dict[var] = day_part
                if var == '?month':
                    month_part = value.split('/')[1]
                    variables_dict[var] = month_part
                if var == '?year':
                    year_part = value.split('/')[2]
                    variables_dict[var] = year_part
    
    new_dict = {key.lstrip('?'): value for key, value in variables_dict.items()}
    return new_dict

def process_csv(csv_file,rules,variable_to_update):
    updated_rows = []
    
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Iterate over each row
        for row in reader:
            # Apply rules to the specified variable in the row
            new_variables = apply_rules_to_value(rules, row[variable_to_update], variable_to_update)
            
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
    value = "12/02/2020"  # Value to which rules will be applied
    rules = read_rules_from_rdf(rdf_file)
    variable_to_update = extract_variables(rules[0])[0]
    process_csv(csv_file, rules, variable_to_update[1:])
