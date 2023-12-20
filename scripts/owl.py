from rdflib import Graph, URIRef
from datetime import datetime

def read_owl_ontology(owl_content):
    g = Graph()
    g.parse(data=owl_content, format="turtle")
    return g

def extract_season_intervals(ontology_graph):
    season_intervals = {}
    for season in ["Winter", "Spring", "Summer", "Autumn"]:
        season_interval_obj = ontology_graph.value(URIRef(f"http://example.org#{season}"), URIRef("http://example.org#hasSeasonInterval"), None)
        if season_interval_obj is not None:
            season_interval = str(season_interval_obj)
            season_intervals[season] = season_interval
    return season_intervals

def infer_season(date_value, season_intervals):
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
    for season, interval in season_intervals.items():
        start_month, start_day, end_month, end_day = map(int, interval.split("/")[0].split("-") + interval.split("/")[1].split("-"))

        # Adjust the condition for Winter to consider the span across two years
        if season == "Winter" and (
            (start_month, start_day) <= (date_obj.month, date_obj.day) or
            (date_obj.month, date_obj.day) <= (end_month, end_day)
        ):
            return season
        elif (start_month, start_day) <= (date_obj.month, date_obj.day) <= (end_month, end_day):
            return season
    return None

# Example OWL ontology content
owl_content = """
@prefix example: <http://example.org#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

example:Winter
    a example:Season ;
    example:hasSeasonInterval "12-21/03-20"^^xsd:string .

example:Spring
    a example:Season ;
    example:hasSeasonInterval "03-21/06-20"^^xsd:string .

example:Summer
    a example:Season ;
    example:hasSeasonInterval "06-21/09-22"^^xsd:string .

example:Autumn
    a example:Season ;
    example:hasSeasonInterval "09-23/12-20"^^xsd:string .
"""

# Read OWL ontology from content
ontology_graph = read_owl_ontology(owl_content)

# Extract season intervals from the ontology
season_intervals = extract_season_intervals(ontology_graph)

# Function to infer season based on date
def get_season_for_date(date_value):
    return infer_season(date_value, season_intervals)

# Example date values
date_value1 = "2023-05-15"
date_value2 = "2000-12-25"
date_value3 = "1900-07-24"
date_value4 = "2001-12-17"

# Infer seasons based on date values
season1 = get_season_for_date(date_value1)
season2 = get_season_for_date(date_value2)
season3 = get_season_for_date(date_value3)
season4 = get_season_for_date(date_value4)

# Print the inferred seasons
print(f"Season for {date_value1}: {season1}")
print(f"Season for {date_value2}: {season2}")
print(f"Season for {date_value3}: {season3}")
print(f"Season for {date_value4}: {season4}")
