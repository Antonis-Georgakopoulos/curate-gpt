import json

def analyze_relationships(data_file):
  """
  Analyzes the relationships in a JSON file.

  Args:
    data_file: The path to the JSON file containing concepts/entities.

  Returns:
    A tuple containing two elements:
      - total_relationships: The total number of distinct relationships found.
      - avg_relationships: The average number of relationships per concept/entity.
  """
  all_relationships = set()
  total_concepts = 0
  concept_relationships = 0
  total_distinct_relationships = 0
  distinct_relationships = []


  # Read data from JSON file
  with open(data_file, 'r') as f:
    data = json.load(f)

  # Process data
  for concept in data:
    concept_set = set()
    relationships = concept["relationships"]

    if relationships is None:
      continue

    concept_relationships += len(relationships)

    for relationship in relationships:
        predicate = relationship["predicate"]
        concept_set.add(predicate)
        all_relationships.add(predicate)

    total_concepts += 1
    total_distinct_relationships += len(concept_set)
    distinct_relationships.extend(list(concept_set))


  total_relationships = len(all_relationships)
  avg_relationships = concept_relationships / total_concepts if total_concepts > 0 else 0
  avg_distinct_relationships = total_distinct_relationships / total_concepts if total_concepts > 0 else 0


  return total_relationships, avg_relationships, avg_distinct_relationships, distinct_relationships

# Example usage
ontologies = ['bao', 'cido', 'doid', 'efo', 'hp', 'ito', 'oba', 'pcl', 'vbo', 'oae']
for ontology in ontologies:
    data_file = f"data\json_{ontology}.json"  # Replace with the actual path to your JSON file

    total_relationships, avg_relationships, avg_distinct_relationships, distinct_relationships  = analyze_relationships(data_file)

    print(f"Info for: {ontology}")
    print(f"Total distinct relationships: {total_relationships}")
    print(f"Average relationships per concept/entity: {avg_relationships:.2f}")
    print(f"Average distinct relationships per concept/entity: {avg_distinct_relationships:.2f}")
    print(f"Distinct Relationships: \n {set(distinct_relationships) }")
    print('\n')