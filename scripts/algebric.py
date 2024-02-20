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
    atom_info['argument_variables'] = arguments
    for atom in atom_list:
        if (atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'), None) in g:
            variable = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'))).split('/')[-1]
            argument = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#argument1'))).split('/')[-1]
            atom_info['argument_variables'][variable] = argument
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
            argument = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#argument1'))).split('/')[-1]
            atom_info[variable] = argument
    head_atoms.append(atom_info)

#print(body_atoms)


for item in head_atoms:
    key = next(iter(item))  # Extract the key from the dictionary
    swrl_rules[key] = body_atoms.pop(0)  # Assign the corresponding body item and remove it from the list

print(swrl_rules)