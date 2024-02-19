from rdflib import Graph, URIRef

# Assuming 'rdf_file.rdf' is the name of your RDF file
g = Graph()
g.parse('/home/rodrirocki/Thesis/ontologies/covid.rdf')

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
    for atom in atom_list:
        if (atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'), None) in g:
            predicate = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#classPredicate'))).split('/')[-1]
            argument = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#argument1'))).split('/')[-1]
            atom_info['class_predicate'] = predicate
            atom_info['class_argument'] = argument
        elif (atom, URIRef('http://www.w3.org/2003/11/swrl#builtin'), None) in g:
            builtin = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#builtin'))).split('/')[-1]
            arguments = next(g.objects(atom, URIRef('http://www.w3.org/2003/11/swrl#arguments'))).split('/')[-1]
            if builtin == 'greaterThan':
                args = arguments.split(',')
                arg1 = args[0].split('/')[-1]
                arg2 = args[1]
                atom_info[builtin] = (arg1, arg2)
            else:
                atom_info[builtin] = arguments
    body_atoms.append(atom_info)

print(body_atoms)
