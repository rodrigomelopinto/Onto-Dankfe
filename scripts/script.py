# generic_templates_script.py

import pandas as pd
from rdflib import Graph, URIRef
from datetime import datetime

def read_templates_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")  # Assuming the ontology is in RDF/XML format
    return g

def process_templates_ontology(ontology_graph, input_csv_path, output_csv_path):
    # Extract variable-operation relationships from the ontology
    variable_operations = {}
    for variable, operation_template in ontology_graph.subject_objects(URIRef("http://example.org#hasOperation")):
        variable = str(variable).split("#")[-1]
        variable_operations.setdefault(variable, []).append(str(operation_template))  
    
    # Read the input CSV file
    df = pd.read_csv(input_csv_path)

    # Process each row in the data frame
    for index, row in df.iterrows():
        for variable, operation_templates in variable_operations.items():
            # Apply the operation rule dynamically based on the ontology
            for operation_template in operation_templates:
                result = apply_operation(row[variable], row, operation_template)
            
                # Update the DataFrame with the new variables
                if result is not None:
                    new_variable_name = [f"{component}" for component in result]
                    df.at[index, new_variable_name[0]] = result[new_variable_name[0]]

    # Save the updated data frame to a new CSV file
    df.to_csv(output_csv_path, index=False)
            
def apply_operation(value, row, operation_template):
    try:
        # Dynamic application of decomposition or mapping based on the ontology
        if "DecompositionTemplate" in operation_template:
            return infer_decomposition(value, operation_template)
        elif "MappingTemplate" in operation_template:
            return infer_mapping(value, operation_template)
        else:
            return None
    except ValueError:
        return None

def infer_decomposition(value, template):
    # Decompose based on the provided template
    components = process_decomposition(templates_ontology_graph, template)
    date_obj = datetime.strptime(value, "%Y-%m-%d")
    for component, query in components.items():
        query_result = date_obj.strftime(query)
        components[component] = query_result
    return components

def infer_mapping(date_value, template):
    # Apply mapping rule dynamically based on the ontology
    components = process_mapping(templates_ontology_graph, template)
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
    result = {}
    variable_name = ""
    for key, value in components.items():
        if key == "variable":
            variable_name = value
    for key, value in components.items():
        if key == "variable":
            continue
        start_date, end_date = map(lambda x: datetime.strptime(x, "%m-%d"), value.split("/"))
        start_date = start_date.replace(year=date_obj.year)
        end_date = end_date.replace(year=date_obj.year)
        if start_date > end_date:
            end_date = end_date.replace(year=date_obj.year + 1)
        if start_date <= date_obj <= end_date:
            result[variable_name] = key
            return result

    return None


def process_decomposition(ontology_graph, operation_template):
    components = {}
    component_query = URIRef(operation_template)
    component_name = ontology_graph.value(component_query, URIRef("http://example.org#hasName"), None)
    component_obj = ontology_graph.value(component_query, URIRef("http://example.org#hasComponent"), None)
    if component_obj is not None:
        component_query = str(component_obj)
        component_name = str(component_name)
        components[component_name] = component_query
        return components


def process_mapping(ontology_graph, operation_template):
    components = {}
    for description in ontology_graph.objects(URIRef(operation_template), URIRef("http://example.org#hasMapping")):
        name = description.split("#")[-1]
        variable_name = ontology_graph.value(URIRef(operation_template), URIRef("http://example.org#hasName"), None)
        interval = ontology_graph.value(description, URIRef("http://example.org#hasMappingInterval"), None)
        if interval is not None:
            components[str(name)] = str(interval)
            components["variable"] = str(variable_name)
    return components
    


# Example templates ontology file path
templates_ontology_file_path = "/home/rodrirocki/Thesis/ontologies/templates.owl"

# Input CSV file path and output CSV file path
templates_input_csv_path = "/home/rodrirocki/Thesis/datasets/test_dataset.csv"
templates_output_csv_path = "/home/rodrirocki/Thesis/datasets/generated_dataset.csv"

# Read templates ontology from the specified file
templates_ontology_graph = read_templates_ontology(templates_ontology_file_path)

# Process the CSV file and create a new CSV file with decomposed and mapped variables
process_templates_ontology(templates_ontology_graph, templates_input_csv_path, templates_output_csv_path)
