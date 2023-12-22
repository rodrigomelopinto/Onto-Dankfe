from rdflib import Graph, URIRef
from datetime import datetime

def read_owl_ontology(owl_content):
    g = Graph()
    g.parse(data=owl_content, format="turtle")
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

# Example OWL ontology content
owl_content = """
@prefix example: <http://example.org#> .

example:YearQuery
    a example:DateComponentQuery ;
    example:hasComponent "%Y" .

example:MonthQuery
    a example:DateComponentQuery ;
    example:hasComponent "%m" .

example:DayQuery
    a example:DateComponentQuery ;
    example:hasComponent "%d" .
"""

# Read OWL ontology from content
ontology_graph = read_owl_ontology(owl_content)

# Extract date components from the ontology
date_components = extract_date_components(ontology_graph)

# Function to infer date components based on date
def get_date_components(date_value):
    return infer_date_components(date_value, date_components)

# Example date value
date_value = "2023-05-15"

# Infer date components based on the date value
components = get_date_components(date_value)

# Print the inferred date components
print(f"Date components for {date_value}: {components}")