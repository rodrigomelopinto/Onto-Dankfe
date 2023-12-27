import re

def infer_decomposition(value, template):
    match = re.match(template, value)
    print(value)
    print(template)
    print(match)

    if match:
        return match.groupdict()

    return {}

# Example usage for date variable
date_value = "14-03-2021"
date_template = "(?P<Day>\\d+)-(?P<Month>\\d+)-(?P<Year>\\d+)"
date_result = infer_decomposition(date_value, date_template)
print("Date Decomposition Result:", date_result)

# Example usage for name variable
name_value = "Rodrigo_Pinto"
name_template = "(?P<first>[^_]+)_(?P<last>[^_]+)"
name_result = infer_decomposition(name_value, name_template)
print("Name Decomposition Result:", name_result)
