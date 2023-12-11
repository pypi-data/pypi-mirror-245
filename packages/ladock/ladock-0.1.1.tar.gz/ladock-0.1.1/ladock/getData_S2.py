import pandas as pd
import numpy as np
import os
from chembl_webresource_client.new_client import new_client
from rdkit import Chem
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from glob import glob

# Function to validate smiles
def validate_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        return Chem.MolToSmiles(mol)
    else:
        return None

def combine_csv_files(target, target_dir):
    # Read all CSV files in the directory
    csv_files = glob(os.path.join(target_dir, '*.csv'))
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return None  # Return None if no files found

    # Read each file and combine them into one DataFrame
    dfs = [pd.read_csv(file) for file in csv_files if os.path.getsize(file) > 0]        
    
    if not dfs:
        print(f"No data in CSV files in the directory {target_dir}.")
        return None  # Return None if no data in files
        
    combined_df = pd.concat(dfs, ignore_index=True)
    output_file = os.path.join(target_dir, f'{target}.csv')
    
    # Save the combined DataFrame to one CSV file
    combined_df.to_csv(output_file, index=False)

    print(f"Data {target_dir} saved in {output_file}")
    return combined_df

def process_chembl_id(chembl_id, target, target_dir):
    try:
        # Load data
        activity = new_client.activity
        res = activity.filter(target_chembl_id=chembl_id).filter(standard_type="IC50")
        df = pd.DataFrame.from_dict(res)

        # Extract columns
        if 'molecule_chembl_id' in df.columns:
            mol_cid = list(df.molecule_chembl_id)
        else:
            mol_cid = []

        if 'canonical_smiles' in df.columns:
            canonical_smiles = list(df.canonical_smiles)
        else:
            canonical_smiles = []

        if 'standard_value' in df.columns:
            standard_value = list(df.standard_value)
        else:
            standard_value = []

        # Create DataFrame with all columns
        data_tuples = list(zip(mol_cid, canonical_smiles, standard_value))
        df = pd.DataFrame(data_tuples, columns=['molecule_chembl_id', 'canonical_smiles', 'standard_value'])

        # Clean and remove duplicates
        df = df.dropna(subset=['molecule_chembl_id'])
        df = df.dropna(subset=['canonical_smiles'])
        df['canonical_smiles'] = df['canonical_smiles'].apply(validate_smiles)
        df = df.drop_duplicates(subset=['molecule_chembl_id'], keep='first', ignore_index=True)

        output_file_path = os.path.join(target_dir, f'{chembl_id}.csv')
        df.to_csv(output_file_path, index=False)

        return f"Processed {chembl_id}"

    except Exception as e:
        return f"Error processing {chembl_id}: {str(e)}"

def getData(chembl_ids, target, target_dir):
    # Use tqdm for progress tracking
    with tqdm(total=len(chembl_ids), desc=f"Processing Chembl IDs for {target}") as pbar:
        max_workers = os.cpu_count() - 2
        futures = []

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Process chembl_ids in parallel
            for chembl_id in chembl_ids:
                future = executor.submit(process_chembl_id, chembl_id, target, target_dir)
                future.add_done_callback(lambda p: pbar.update())
                futures.append(future)

        # Wait for all tasks to complete
        results = [future.result() for future in futures]

    # Display results
    for result in results:
        print(result)

    # After creating CSV files, combine them all
    combined_df = combine_csv_files(target, target_dir)
    return combined_df
    
if __name__ == "__main__":
    # Set the random seed for reproducibility
    np.random.seed(1)

    current_dir = os.getcwd()
    targets_files = glob(os.path.join(current_dir, 'targets_*.csv'))
    df_all_target = []
    targets = []

    for targets_file_path in targets_files:
        with open(targets_file_path, 'r') as targets_file:
            chembl_ids = pd.read_csv(targets_file_path)['target_chembl_id']       
            target = os.path.splitext(os.path.basename(targets_file_path))[0].replace("targets_", "")
            target_dir = os.path.join(current_dir, target.replace(" ", "-"))

            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            
            combined_df = getData(chembl_ids, target, target_dir)
            if combined_df is not None:
                df_all_target.append(combined_df)
                targets.append(target)

    if df_all_target:
        # Combine all DataFrames
        df_combined = pd.concat(df_all_target, ignore_index=True)

        # Save the combined DataFrame to one CSV file
        csv_all_target = os.path.join(current_dir, '_'.join(targets) + '.csv')
        df_combined.to_csv(csv_all_target, index=False)

        print(f"Data all targets saved in {csv_all_target}")
    else:
        print("No data to combine.")

