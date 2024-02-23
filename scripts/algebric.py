import csv
from rdflib import Graph, URIRef, Literal

# Assuming 'rdf_file.rdf' is the name of your RDF file
g = Graph()
g.parse('/home/rodrirocki/Thesis/ontologies/covid.rdf')

swrl_rules = {}

body_atoms = []

for s, p, o in g.triples((None, URIRef('http://www.w3.org/2003/11/swrl#body'), None)):
    atom_list = [o]
    while True:
        for s, p, o in g.triples((atom_list[-1], URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#first'), None)):
            atom_list.append(o)
        rest = next(g.objects(atom_list[-2], URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#rest')))
        if rest == URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#nil'):
            break
        atom_list.append(rest)

    atom_info = {}
    arguments = {}
    list_builtin = []
    variables_connection = {}
    atom_info['argument_variables'] = arguments
    for atom in atom_list:
        if (atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'), None) in g:
            variable = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'))).split('/')[-1]
            argument = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#argument1'))).split('/')[-1]
            variables_connection[argument] = variable
            atom_info['argument_variables'][variable] = variable
        elif (atom, URIRef('http://www.w3.org/2003/11/swrl#builtin'), None) in g:
            builtin = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#builtin'))).split('/')[-1]
            arguments = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#arguments'))).split('/')[-1]
            arguments = list(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#arguments')))
            for arg in arguments:
                list_items = {}
                list_items[builtin.split('#')[-1]] = []
                for item in g.items(arg):
                    # If the list item is a resource, print its URI
                    if isinstance(item, URIRef):
                        if str(item).split('/')[-1] in variables_connection:
                            list_items[builtin.split('#')[-1]].append(variables_connection[str(item).split('/')[-1]])
                        else:
                            list_items[builtin.split('#')[-1]].append(str(item).split('/')[-1])
                    # If the list item is a literal, print its value
                    elif isinstance(item, Literal):
                        list_items[builtin.split('#')[-1]].append(str(item))
                list_builtin.append(list_items)
            atom_info['builtins'] = list_builtin
    body_atoms.append(atom_info)


head_atoms = []

for s, p, o in g.triples((None, URIRef('http://www.w3.org/2003/11/swrl#head'), None)):
    atom_list = [o]
    while True:
        for s, p, o in g.triples((atom_list[-1], URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#first'), None)):
            atom_list.append(o)
        rest = next(g.objects(atom_list[-2], URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#rest')))
        if rest == URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#nil'):
            break
        atom_list.append(rest)

    atom_info = {}
    arguments = {}
    list_builtin = []
    for atom in atom_list:
        if (atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'), None) in g:
            variable = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'))).split('/')[-1]
            atom_info[variable] = variable
    head_atoms.append(atom_info)


for item in head_atoms:
    key = next(iter(item))  # Extract the key from the dictionary
    swrl_rules[key] = body_atoms.pop(0)  # Assign the corresponding body item and remove it from the list



def apply_swrl_rules_to_row(row, swrl_rules):
    intermediate_results = {}
    
    for rule_name, rule in swrl_rules.items():
        operations = rule['builtins']
        final_operation = operations[-1]
        
        # Perform intermediate operations
        for ops in operations[:-1]:
            op_type = list(ops.keys())[0]
            args = ops[op_type]
            arg1, arg2, arg3 = args
            if row[arg2] == '' or row[arg3] == '':
                intermediate_results[arg1] = None
                continue
            if op_type == 'divide':
                try:
                    result = float(row[arg2]) / float(row[arg3])
                except ZeroDivisionError:
                    result = None
                intermediate_results[arg1] = result
            elif op_type == 'multiply':
                result = float(row[arg2]) * float(row[arg3])
                intermediate_results[arg1] = result
    
        final_op_type = list(final_operation.keys())[0]
        final_op_args = final_operation[final_op_type]
        
        # Perform final operation
        if final_op_type == 'multiply':
            arg1, arg2, arg3 = final_op_args
            if arg2 in intermediate_results and intermediate_results[arg2] is not None:
                if arg3.isdigit():
                    result = intermediate_results[arg2] * int(arg3)
                else:
                    result = intermediate_results[arg2] * row[arg3]
                row[rule_name] = result
                continue
            if arg3 in intermediate_results and intermediate_results[arg3] is not None:
                if arg2.isdigit():
                    result = int(arg2) * intermediate_results[arg3]
                else:
                    result = row[arg2] * intermediate_results[arg3]
                row[rule_name] = result
                continue
            if arg2 in intermediate_results and intermediate_results[arg2] is None:
                row[rule_name] = None
                continue
            if arg3 in intermediate_results and intermediate_results[arg3] is None:
                row[rule_name] = None
                continue
            if arg2.isdigit():
                result = int(arg2) * int(row[arg3])
                row[rule_name] = result
                continue
            if arg3.isdigit():
                result = int(row[arg2]) * int(arg3)
                row[rule_name] = result
                continue
            result = int(row[arg2]) * int(row[arg3])
            row[rule_name] = result
            continue
        if final_op_type == 'divide':
            arg1, arg2, arg3 = final_op_args
            if arg2 in intermediate_results and intermediate_results[arg2] is not None:
                if arg3.isdigit():
                    try:
                        result = intermediate_results[arg2] / int(arg3)
                    except ZeroDivisionError:
                        result = None
                    row[rule_name] = result
                    continue
                else:
                    try:
                        result = intermediate_results[arg2] / int(row[arg3])
                    except ZeroDivisionError:
                        result = None
                    row[rule_name] = result
                    continue
            if arg3 in intermediate_results and intermediate_results[arg3] is not None:
                if arg2.isdigit():
                    try:
                        result = int(arg2) / intermediate_results[arg3]
                    except ZeroDivisionError:
                        result = None
                    row[rule_name] = result
                    continue
                else:
                    try:
                        result = int(row[arg2]) / intermediate_results[arg3]
                    except ZeroDivisionError:
                        result = None
                    row[rule_name] = result
                    continue
            if arg2 in intermediate_results and intermediate_results[arg2] is None:
                row[rule_name] = None
                continue
            if arg3 in intermediate_results and intermediate_results[arg3] is None:
                row[rule_name] = None
                continue
            if arg2.isdigit():
                try:
                    result = int(arg2) / int(row[arg3])
                except ZeroDivisionError:
                    result = None
                row[rule_name] = result
                continue
            if arg3.isdigit():
                try:
                    result = int(row[arg2]) / int(arg3)
                except ZeroDivisionError:
                    result = None
                row[rule_name] = result
                continue
            try:
                result = int(row[arg2]) / int(row[arg3])
            except ZeroDivisionError:
                result = None
            row[rule_name] = result
            continue
        # Add conditions for other final operations if needed
    
    return row


def apply_swrl_rules_to_dataset(csv_file, swrl_rules):
    modified_dataset = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            modified_row = apply_swrl_rules_to_row(row, swrl_rules)
            modified_dataset.append(modified_row)
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = modified_dataset[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in modified_dataset:
            writer.writerow(row)


# Apply SWRL rules to the dataset
modified_dataset = apply_swrl_rules_to_dataset('/home/rodrirocki/Thesis/case_study/Oceania_covid_data.csv', swrl_rules)
