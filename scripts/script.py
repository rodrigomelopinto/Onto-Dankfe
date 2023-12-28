# generic_templates_script.py

import pandas as pd
import math
import re
from rdflib import Graph, URIRef
from datetime import datetime

def read_templates_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")  # Assuming the ontology is in RDF/XML format
    return g

def process_templates_ontology(ontology_graph, input_csv_path, output_csv_path):
    variable_operations = {}
    
    for variable, operation_template in ontology_graph.subject_objects(URIRef("http://example.org#hasOperation")):
        variable = str(variable).split("#")[-1]
        operation_template = str(operation_template)
        
        if "MappingTemplate" in operation_template:
            variable_operations.setdefault("mapping", {}).setdefault(variable, []).append(operation_template)
        elif "DecompositionTemplate" in operation_template:
            variable_operations.setdefault("decomposition", {}).setdefault(variable, []).append(operation_template)
        elif "AlgebraicTemplate" in operation_template:
            variable_operations.setdefault("algebraic", {}).setdefault(variable, []).append(operation_template)

    
    df = pd.read_csv(input_csv_path)
    
    for index, row in df.iterrows():
        for variable_type, operations in variable_operations.items():
            for variable, operation_templates in operations.items():
                for operation_template in operation_templates:
                    if variable_type == "mapping":
                        result = infer_mapping(row[variable], operation_template)
                    elif variable_type == "decomposition":
                        result = infer_decomposition(row[variable], operation_template)
                    elif variable_type == "algebraic":
                        result = perform_algebraic_operation(operation_template, row)

                    new_variable = get_variable_name(operation_template)

                    if result is not None:
                        df.at[index, new_variable] = result[new_variable]

    df.to_csv(output_csv_path, index=False)


def perform_algebraic_operation(operation_template, row):
    query = URIRef(operation_template)
    new_variable = get_variable_name(operation_template)
    result = None
    operands = []
    operation_type = templates_ontology_graph.value(query, URIRef("http://example.org#hasOperationType"), None)
    for operand in templates_ontology_graph.objects(query, URIRef("http://example.org#hasOperand")):
        operands.append(str(operand).split("#")[-1])
    # Extract values of the variables involved in the algebraic operation
    variable_data = {operand: row[operand] for operand in operands}

    if "+" in operation_type:
        return {new_variable: sum(variable_data.values())}
    elif "/" in operation_type:
        if variable_data[operands[1]] == 0:
            return {new_variable: None}
        return {new_variable: round(variable_data[operands[0]] / variable_data[operands[1]], 1)}
    elif "*" in operation_type:
        for operand in operands:
            result = result * variable_data[operand] if result is not None else variable_data[operand]
        return {new_variable: result}
    elif "-" in operation_type:
        for operand in operands:
            result = result - variable_data[operand] if result is not None else variable_data[operand]
        return {new_variable: result}
    elif "abs" in operation_template:
        return {new_variable: abs(variable_data[operands[0]])}
    elif "sqrt" in operation_template:
        return {new_variable: round(variable_data[operands[0]] ** 0.5, 1)}
    elif "log" in operation_template:
        return {new_variable: round(math.log(variable_data[operands[0]]), 1)}
    # Add more cases for other algebraic operations as needed



def infer_decomposition(value, template):
    # Decompose based on the provided template
    decomposition_template = process_decomposition(templates_ontology_graph, template)
    match = re.match(decomposition_template, value)

    if match:
        return match.groupdict()

    return {}

def infer_mapping(date_value, template):
    # Apply mapping rule dynamically based on the ontology
    components = process_mapping(templates_ontology_graph, template)
    variable = get_variable_name(template)
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
    result = {}
    for key, value in components.items():
        start_date, end_date = map(lambda x: datetime.strptime(x, "%m-%d"), value.split("/"))
        start_date = start_date.replace(year=date_obj.year)
        end_date = end_date.replace(year=date_obj.year)
        if start_date > end_date:
            if date_obj >= start_date or date_obj <= end_date.replace(year=date_obj.year + 1):
                result[variable] = key
            
        else:
            if start_date <= date_obj <= end_date:
                result[variable] = key

    return result if result else None


def get_variable_name(operation_template):
    # Get the name of the variable from the operation template
    query = URIRef(operation_template)
    variable_name = templates_ontology_graph.value(query, URIRef("http://example.org#hasName"), None)
    if variable_name is not None:
        return str(variable_name).split("#")[-1]
    return None



def process_decomposition(ontology_graph, operation_template):
    decomposition_template = ""
    query = URIRef(operation_template)
    template = ontology_graph.value(query, URIRef("http://example.org#hasDecompositionTemplate"), None)
    if template is not None:
        decomposition_template = str(template)
        return decomposition_template


def process_mapping(ontology_graph, operation_template):
    components = {}
    for description in ontology_graph.objects(URIRef(operation_template), URIRef("http://example.org#hasMapping")):
        name = description.split("#")[-1]
        interval = ontology_graph.value(description, URIRef("http://example.org#hasMappingInterval"), None)
        if interval is not None:
            components[str(name)] = str(interval)
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
