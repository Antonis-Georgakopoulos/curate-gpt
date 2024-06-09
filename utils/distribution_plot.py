import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def analyze_relationships(data_file):
    """
    Analyzes the relationships in a JSON file and returns a list of number of relationships for each entity.

    Args:
        data_file: The path to the JSON file containing concepts/entities.

    Returns:
        A list of integers representing the number of relationships for each entity.
    """
    # Read data from JSON file
    with open(data_file, 'r') as f:
        data = json.load(f)

    # Process data and extract number of relationships
    num_relationships = [0 if concept.get("relationships", []) is None else len(concept.get("relationships", [])) for concept in data]

    return num_relationships

# Example usage
data_file1 = "data/structured/elsst.json"  # Replace with the actual path to your first JSON file
data_file2 = "data/json_bao.json"  # Replace with the actual path to your second JSON file

# Get list of number of relationships for both datasets
num_relationships1 = analyze_relationships(data_file1)
num_relationships2 = analyze_relationships(data_file2)

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Plot the histogram for the first dataset
axs[0].hist(num_relationships1, bins=range(min(num_relationships1), max(num_relationships1) + 1), alpha=0.7, edgecolor='black', log=True)
axs[0].set_xlabel('Number of Relationships')
axs[0].set_ylabel('Number of Concepts/Classes (Log Scale)')
axs[0].set_title('Distribution of Number of Relationships in ELSST')

# Plot the histogram for the second dataset
axs[1].hist(num_relationships2, bins=range(min(num_relationships2), max(num_relationships2) + 1), alpha=0.7, edgecolor='black', log=True)
axs[1].set_xlabel('Number of Relationships')
axs[1].set_ylabel('Number of Concepts/Classes (Log Scale)')
axs[1].set_title('Distribution of Number of Relationships in BAO')
axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
