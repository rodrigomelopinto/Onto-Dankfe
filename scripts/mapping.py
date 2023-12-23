import pandas as pd
from rdflib import Graph, URIRef
from datetime import datetime

def read_season_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="xml")  # Assuming the ontology is in RDF/XML format
    return g

def infer_season(date_value, season_intervals):
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")

    for season, interval in season_intervals.items():
        start_date, end_date = map(lambda x: datetime.strptime(x, "%m-%d"), interval.split("/"))
        start_date = start_date.replace(year=date_obj.year)
        end_date = end_date.replace(year=date_obj.year)
        if start_date > end_date:
            end_date = end_date.replace(year=date_obj.year + 1)
        if start_date <= date_obj <= end_date:
            return season

    return None  # Return None if no matching season is found

def process_season_csv(input_csv_path, output_csv_path, ontology_graph):
    # Read the input CSV file
    df = pd.read_csv(input_csv_path)

    # Extract season intervals from the ontology
    season_intervals = {}
    for season in ["Winter", "Spring", "Summer", "Autumn"]:
        season_interval_obj = ontology_graph.value(URIRef(f"http://example.org#{season}"), URIRef("http://example.org#hasSeasonInterval"), None)
        if season_interval_obj is not None:
            season_intervals[season] = str(season_interval_obj)

    # Create a new column for Season
    df["Season"] = ""

    # Process each row in the data frame
    for index, row in df.iterrows():
        date_value = row["Date"]  # Assuming the "Date" column in the CSV contains date values


        # Infer season based on the date value
        season = infer_season(date_value, season_intervals)

        # Store the season for each row
        df.at[index, "Season"] = season

    # Save the updated data frame to a new CSV file
    df.to_csv(output_csv_path, index=False)

# Example season ontology file path
season_ontology_file_path = "/home/rodrirocki/Thesis/ontologies/mapping.owl"

# Read season ontology from the specified file
season_ontology_graph = read_season_ontology(season_ontology_file_path)

# Input CSV file path and output CSV file path
season_input_csv_path = "/home/rodrirocki/Thesis/datasets/test_dataset.csv"
season_output_csv_path = "/home/rodrirocki/Thesis/datasets/generated_dataset.csv"

# Process the CSV file and create a new CSV file with the Season variable
process_season_csv(season_input_csv_path, season_output_csv_path, season_ontology_graph)
