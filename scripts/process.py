import pandas as pd
from rdflib import Graph, URIRef
from decomposition import infer_date_components
from mapping import infer_season

def read_combined_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")  # Assuming the ontology is in RDF/XML format
    return g

def process_ontology(ontology_graph):
    # Extract date components from the ontology
    date_components = {}
    for component in ["Year", "Month", "Day"]:
        component_query = URIRef(f"http://example.org#{component}Query")
        date_component_obj = ontology_graph.value(component_query, URIRef("http://example.org#hasComponent"), None)
        if date_component_obj is not None:
            date_component_query = str(date_component_obj)
            date_components[component] = date_component_query

    # Extract season intervals from the ontology
    season_intervals = {}
    for season in ["Winter", "Spring", "Summer", "Autumn"]:
        season_interval_obj = ontology_graph.value(URIRef(f"http://example.org#{season}"), URIRef("http://example.org#hasSeasonInterval"), None)
        if season_interval_obj is not None:
            season_intervals[season] = str(season_interval_obj)

    return date_components, season_intervals

def process_csv(input_csv_path, output_csv_path, ontology_graph):
    # Read the input CSV file
    df = pd.read_csv(input_csv_path)

    # Extract date components and season intervals from the ontology
    date_components, season_intervals = process_ontology(ontology_graph)

    # Create new columns for Day, Month, Year, and Season
    df["Day"] = ""
    df["Month"] = ""
    df["Year"] = ""
    df["Season"] = ""

    # Process each row in the data frame
    for index, row in df.iterrows():
        date_value = row["Date"]  # Assuming the "Date" column in the CSV contains date values

        # Infer date components based on the date value
        components = infer_date_components(date_value, date_components)

        # Infer season based on the date value
        season = infer_season(date_value, season_intervals)

        # Store the components for each row
        df.at[index, "Day"] = components["Day"]
        df.at[index, "Month"] = components["Month"]
        df.at[index, "Year"] = components["Year"]
        df.at[index, "Season"] = season

    # Save the updated data frame to a new CSV file
    df.to_csv(output_csv_path, index=False)

ontology_path = "/home/rodrirocki/Thesis/ontologies/decomposition_mapping.owl"

ontology_graph = read_combined_ontology(ontology_path)

input_csv_path = "/home/rodrirocki/Thesis/datasets/test_dataset.csv"
output_csv_path = "/home/rodrirocki/Thesis/datasets/generated_dataset.csv"

process_csv(input_csv_path, output_csv_path, ontology_graph)