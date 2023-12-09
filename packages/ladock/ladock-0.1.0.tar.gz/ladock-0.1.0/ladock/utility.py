import requests
from tqdm import tqdm
from retrying import retry
import os
import subprocess
import gzip
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from requests.exceptions import RequestException
from time import sleep
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from os.path import basename, splitext
from concurrent.futures import ThreadPoolExecutor, as_completed
from Bio.PDB import PDBParser

def sort_and_add_number(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Print the columns of the DataFrame
    print("Columns in DataFrame:", df.columns)

    # Remove leading and trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Sort the DataFrame by 'ligand_id' and 'docking_score' in ascending order
    df_sorted = df.sort_values(by=['docking_score'], ascending=[True])

    # Keep the row with the lowest 'docking_score' for each 'ligand_id'
    df_filtered = df_sorted.drop_duplicates(subset='ligand_id', keep='first')

    # Add a 'No' column with consecutive numbers
    df_filtered.insert(0, 'No', range(1, len(df_filtered) + 1))

    # Save the result back to the CSV file
    df_filtered.to_csv(csv_file, index=False)
    print(df_filtered)

# Define the maximum number of retries and delay between retries (in seconds)
max_retries = 3
retry_delay = 1  # 1 second

def download_file_with_retry(url, destination):
    for attempt in range(max_retries):
        try:
            print(f"Downloading URL: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024000  # 1000 KB
            t = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', dynamic_ncols=True)

            with open(destination, 'wb') as file:
                for data in response.iter_content(chunk_size=block_size):
                    file.write(data)
                    t.update(len(data))

            t.close()
            return  # Successful download, exit the function

        except RequestException as e:
            print(f"Attempt {attempt + 1} failed. Error: {e}")

        except Exception as e:
            print(f"Unexpected error during file download. Error: {e}")

        # Wait before the next retry
        sleep(retry_delay)

    print(f"Failed to download {url} after {max_retries} attempts.")

def extract_gz(file_path):
    with gzip.open(file_path, 'rb') as f_in, open(file_path[:-3], 'wb') as f_out:
        f_out.write(f_in.read())
        
def run_command(command):
    subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def prepare_ligand(ligand_pdb, mgl_directory):
    prepare_path = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_ligand4.py") 
    run_command(f'{prepare_path} -l {ligand_pdb}')
    return

def prepare_receptor(receptor_pdb, mgl_directory):
    prepare_path = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_receptor4.py")
    run_command(f'{prepare_path} -r {receptor_pdb}')
    return

def convert_to_smiles(input_file):
    try:
        output_file = "smiles.smi"
        obabel_command = f'obabel {input_file} -osmi -O {output_file}'
        subprocess.run(obabel_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(output_file, 'r') as smiles_file:
            smiles = smiles_file.read().strip()
        os.remove(output_file)
        smiles = smiles.split('\t')[0]
        return smiles
    except Exception as e:        
        return None

def delete_files_except_pdb(receptor_pdb, reference_pdb):
    for filename in os.listdir('.'):
        if filename not in [receptor_pdb, reference_pdb]:
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Error deleting file {filename}: {e}")

def print_dev(developer_note, developer_contact, citation_list):
    print("")
    print(developer_note)
    print("")
    print(developer_contact)
    print("")
    print(citation_list)
    print("")
