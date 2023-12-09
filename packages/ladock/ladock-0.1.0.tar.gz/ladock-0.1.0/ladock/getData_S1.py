import os
import numpy as np
import pandas as pd
from chembl_webresource_client.new_client import new_client

np.random.seed(1)

# Load target data
target = new_client.target

query_file_path = 'chembl_query.txt'  # Update with the correct file path

with open(query_file_path, 'r') as query_file:
    for search_term in query_file:
        search_term = search_term.strip()
        
        # Perform target search
        target_query = target.search(search_term)
        targets = pd.DataFrame.from_dict(target_query)

        # Select columns and include search_term
        search_term = search_term.replace(" ", "-")
        selected_columns = ['target_chembl_id', 'pref_name', 'search_term']
        targets['search_term'] = search_term  # Add search_term column
        targets = targets[selected_columns]

        # Save DataFrame to CSV
        current_dir = os.getcwd()
        targets_output_file_path = os.path.join(current_dir, f'targets_{search_term}.csv')
        targets.to_csv(targets_output_file_path, index=False)
        print(f"Targets for search term '{search_term}' saved to {targets_output_file_path}")

