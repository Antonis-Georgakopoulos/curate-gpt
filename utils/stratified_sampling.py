import json
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the JSON data
with open('data\structured\elsst.json', 'r') as f:
    data = json.load(f)

# Create a DataFrame from the JSON data
df = pd.DataFrame(data)

# Count the number of relationships for each entity
df['num_relationships'] = df['relationships'].apply(lambda x: len(x) if x is not None else 0)

# Define custom bins for the 'num_relationships' feature
# FOR BAO
# bins = [0, 1, 2, 3, df['num_relationships'].max()+1]
# labels = ['0-1', '1-2', '2-3', '3+']

# FOR ELSST
bins = [0, 2, 6, 11, df['num_relationships'].max()+1]
labels = ['0-2', '3-6', '7-11', '12+']

# Assign bin labels to each entity
df['relationship_bin'] = pd.cut(df['num_relationships'], bins=bins, labels=labels, include_lowest=True)

# Perform stratified sampling based on the bin labels
train_set, eval_set = train_test_split(df, test_size=200, stratify=df['relationship_bin'])


# Verify the distribution
print("Training set distribution:\n", train_set['relationship_bin'].value_counts())
print("Evaluation set distribution:\n", eval_set['relationship_bin'].value_counts())



train_set_dict = train_set.to_dict(orient='records')
eval_set_dict = eval_set.to_dict(orient='records')



for entity in train_set_dict:
  entity.pop("num_relationships", None)
  entity.pop("relationship_bin", None)

for entity in eval_set_dict:
  entity.pop("num_relationships", None)
  entity.pop("relationship_bin", None)





import copy
# Make a copy of the training set to avoid modifying the original
train_set_modified = copy.deepcopy(train_set_dict)

# Iterate over entities in the evaluation set
for entity in eval_set_dict:
    entity_label = entity['id']

    # Iterate over entities in the training set
    for train_entity in train_set_modified:
        relationships = train_entity['relationships']
        modified_relationships = []

        if relationships is None:
            continue
        
        # Iterate over relationships and remove those with target matching entity_label
        for relationship in relationships:
            if relationship['target'] != entity_label:
                modified_relationships.append(relationship)

        # Update the relationships in the training set
        train_entity['relationships'] = modified_relationships




# Save the training set as a JSON file with indentation
with open('elsst_train_set_less.json', 'w') as f:
    json.dump(train_set_modified, f, indent=4)

# Save the evaluation set as a JSON file with indentation
with open('elsst_eval_set_less.json', 'w') as f:
    json.dump(eval_set_dict, f, indent=4)

