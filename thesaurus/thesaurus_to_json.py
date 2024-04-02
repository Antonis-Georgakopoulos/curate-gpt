from rdflib import Graph, Namespace


def getProperty(g, concept_uri, prop, language='en'):
    """
    Based on a specific concept and a language return the property on that specific language 
    """

    # Find all triples with the specified Concept URI and the property
    triples = g.triples((concept_uri, prop, None))

    for s, p, o in triples:

        if o.language == language:
            return o
    
    return ''


def convert_to_camel_case(input_text):
    """
    Converts input_text to camel case by capitalizing the first letter of each word
    and removing spaces.
    """
    # split the input text into words
    words = input_text.split()  
    camel_case_words = [word.capitalize() for word in words]
    return ''.join(camel_case_words) 


if __name__ == '__main__':

    # Load the RDF/XML file
    g = Graph()
    g.parse("data\ELSST_R4.rdf")

    # Define namespaces
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    skos = Namespace("http://www.w3.org/2004/02/skos/core#")

    language = 'en'

    # Define the JSON structure
    concepts = []

    # Iterate over each Concept
    for concept_uri in g.subjects(rdf.type, skos.Concept):
        concept = dict()
        concept["uri"] = concept_uri.toPython()

        prefLabel = getProperty(g, concept_uri, skos.prefLabel, language)
        concept["prefLabel"] = prefLabel

        definition = getProperty(g, concept_uri, skos.definition, language)
        concept["definition"] = definition

        altLabel = getProperty(g, concept_uri, skos.altLabel, language)
        concept["altLabel"] = altLabel

        id = convert_to_camel_case(prefLabel)
        concept["id"] = id

        # get relationships
        concept["relationships"] = []
        for rel, target in g.predicate_objects(concept_uri):
            if rel == skos.related or rel == skos.narrower or rel == skos.broader or rel == skos.topConceptOf:
                relationship = {"predicate": rel.split("#")[-1], "target": getProperty(g, target, skos.prefLabel, language)}
                concept["relationships"].append(relationship)

        concepts.append(concept)


    # Save the result to a JSON file
    import json

    with open("data\output.json", "w") as json_file:
        json.dump(concepts, json_file, indent=4)
