import rdflib
import json

# Load the OWL file
graph = rdflib.Graph()
g.parse("data\ELSST_R4.rdf")

# Define namespaces
namespace_manager = rdflib.namespace.NamespaceManager(graph)
namespace_manager.bind('owl', rdflib.namespace.OWL)
namespace_manager.bind('rdfs', rdflib.namespace.RDFS)
namespace_manager.bind('obo', rdflib.URIRef("http://purl.obolibrary.org/obo/"))

# Initialize the JSON object
json_obj = []

# Iterate over each class in the OWL file
for s, p, o in graph.triples((None, rdflib.namespace.RDF.type, rdflib.namespace.OWL.Class)):
    class_obj = {
        "id": str(s),
        "relationships": [],
        "label": "",
        "definition": ""
    }

    # Iterate over each relationship for the current class
    for s2, p2, o2 in graph.triples((s, None, None)):
        if p2 != rdflib.namespace.RDF.type:
            # Get the label for the predicate
            predicate_label = [str(o) for o in graph.objects(p2, rdflib.namespace.RDFS.label)]
            predicate_label = predicate_label[0] if predicate_label else str(p2)

            # Get the label for the target
            target_label = [str(o) for o in graph.objects(o2, rdflib.namespace.RDFS.label)]
            target_label = target_label[0] if target_label else str(o2)

            relationship = {
                "predicate": predicate_label,
                "target": target_label
            }
            class_obj["relationships"].append(relationship)

        # Get the label for each concept
        if p2 == rdflib.namespace.RDFS.label:
            class_obj["label"] = str(o2)

        # Get the definition for each concept
        if p2 == rdflib.URIRef("http://purl.obolibrary.org/obo/IAO_0000115"):
            class_obj["definition"] = str(o2)

    # Add the class object to the JSON object
    json_obj.append(class_obj)

# Convert the JSON object to a string
json_str = json.dumps(json_obj, indent=4)

# Write the JSON string to a file
with open("output.json", "w") as outfile:
    outfile.write(json_str)
