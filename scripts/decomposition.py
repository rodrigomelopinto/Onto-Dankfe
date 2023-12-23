import pandas as pd
from rdflib import Graph, URIRef
from datetime import datetime

def read_owl_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")  # Assuming the ontology is in RDF/XML format
    return g

def extract_date_components(ontology_graph):
    date_components = {}
    for component in ["Year", "Month", "Day"]:
        component_query = URIRef(f"http://example.org#{component}Query")
        date_component_obj = ontology_graph.value(component_query, URIRef("http://example.org#hasComponent"), None)
        if date_component_obj is not None:
            date_component_query = str(date_component_obj)
            date_components[component] = date_component_query
    return date_components

def infer_date_components(date_value, date_components):
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
    components = {}
    for component, query in date_components.items():
        query_result = date_obj.strftime(query)
        components[component] = query_result
    return components

def process_csv(input_csv_path, output_csv_path, ontology_graph):
    # Read the input CSV file
    df = pd.read_csv(input_csv_path)

    # Extract date components from the ontology
    date_components = extract_date_components(ontology_graph)

    # Create new columns for Day, Month, and Year
    df["Day"] = ""
    df["Month"] = ""
    df["Year"] = ""

    # Process each row in the data frame
    for index, row in df.iterrows():
        date_value = row["Date"]  # Assuming the "Date" column in the CSV contains date values

        # Infer date components based on the date value
        components = infer_date_components(date_value, date_components)

        # Store the components for each row
        df.at[index, "Day"] = components["Day"]
        df.at[index, "Month"] = components["Month"]
        df.at[index, "Year"] = components["Year"]

    # Save the updated data frame to a new CSV file
    df.to_csv(output_csv_path, index=False)

# Example OWL ontology file path
owl_file_path = "/home/rodrirocki/Thesis/ontologies/test.owl"

# Read OWL ontology from the specified file
ontology_graph = read_owl_ontology(owl_file_path)

# Input CSV file path and output CSV file path
input_csv_path = "/home/rodrirocki/Thesis/datasets/test_dataset.csv"
output_csv_path = "/home/rodrirocki/Thesis/datasets/generated_dataset.csv"

# Process the CSV file and create a new CSV file with date components
process_csv(input_csv_path, output_csv_path, ontology_graph)
