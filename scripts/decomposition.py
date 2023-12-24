from datetime import datetime

def infer_date_components(date_value, date_components):
    date_obj = datetime.strptime(date_value, "%Y-%m-%d")
    components = {}
    for component, query in date_components.items():
        query_result = date_obj.strftime(query)
        components[component] = query_result
    return components
