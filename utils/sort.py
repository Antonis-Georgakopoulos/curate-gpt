import json

def analyze_and_sort_relationships1(data_file):
  """
  Analyzes and sorts relationships in a JSON file.

  Args:
    data_file: The path to the JSON file containing concepts/entities.

  Returns:
    A list of dictionaries, where each dictionary represents a concept/entity with its:
      - id: The entity's ID.
      - label: The entity's label.
      - num_relationships: The number of relationships for the entity.
  """
  # Read data from JSON file
  with open(data_file, 'r') as f:
    data = json.load(f)

  # Process data using list comprehension and sort by relationships (descending)
  return sorted([
      {"id": concept["id"]
       , "label": concept["label"]
       , "definition": concept["definition"]
       , "aliases": concept["aliases"]
       , "logical_definition": concept["logical_definition"]
       , "original_id": concept["original_id"]
       , "relationships": concept["relationships"]
       , "num_relationships": 0 if concept.get("relationships", []) is None else len(concept.get("relationships", []))
       }
      for concept in data
  ], key=lambda x: x["num_relationships"], reverse=True)



def analyze_and_sort_relationships2(data_file):
  """
  Analyzes and sorts relationships in a JSON file.

  Args:
    data_file: The path to the JSON file containing concepts/entities.

  Returns:
    A list of dictionaries, where each dictionary represents a concept/entity with its:
      - id: The entity's ID.
      - label: The entity's label.
      - num_relationships: The number of relationships for the entity.
  """
  # Read data from JSON file
  with open(data_file, 'r') as f:
    data = json.load(f)

  # Process data using list comprehension and sort by relationships (descending)
  return sorted([
      {"uri": concept["uri"]
       , "prefLabel": concept["prefLabel"]
       , "definition": concept["definition"]
       , "altLabel": concept["altLabel"]
       , "id": concept["id"]
       , "relationships": concept["relationships"]
       , "num_relationships": 0 if concept.get("relationships", []) is None else len(concept.get("relationships", []))
       }
      for concept in data
  ], key=lambda x: x["num_relationships"], reverse=True)



# Example usage
data_file1 = "data\json_bao.json"  # Replace with the actual path to file 1
data_file2 = "data\structured\elsst.json"  # Replace with the actual path to file 2

sorted_entities1 = analyze_and_sort_relationships1(data_file1)
for entity in sorted_entities1:
  entity.pop("num_relationships", None)

sorted_entities2 = analyze_and_sort_relationships2(data_file2)
for entity in sorted_entities2:
  entity.pop("num_relationships", None)


# Save sorted entities to separate JSON files
with open("sorted_bao.json", "w") as f:
  json.dump(sorted_entities1, f, indent=4)  # Indent for readability

with open("sorted_elsst.json", "w") as f:
  json.dump(sorted_entities2, f, indent=4)

print("\nEntities saved")
