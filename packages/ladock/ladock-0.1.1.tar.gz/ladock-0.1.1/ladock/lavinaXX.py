import os
import requests
import gzip
from tqdm import tqdm
from multiprocessing import Pool
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from os.path import basename, splitext
from main import *
from functools import partial
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures

from utility import (
    process_reference_vina,  
    print_dev,
    delete_files_except_pdb,
    process_ligand_test,
    sort_and_add_number  

)
     
def main():
    os.chdir(current_directory)
    model_dirs = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d)) and d.startswith('model')]
    ligand_dir = os.path.join(current_directory, 'ligand_input')
    output_dir = os.path.join(current_directory, 'output')
    config_file = os.path.join(current_directory, 'config_lavina.txt')

    config_variables = {}
    with open(config_file, 'r') as config_file:
        config_lines = config_file.readlines()

    for line in config_lines:
        if not line.strip().startswith('#'):
            try:
                name, value = line.strip().split('=')
                name = name.strip()
                value = value.strip()
                config_variables[name] = value
            except ValueError:
                # Handle the exception (add more lines as needed)
                pass

    mgl_directory = config_variables['mgl_directory']
    
    ensamble = 'vina' 
    num_modes = int(config_variables['num_modes'])  # Konversi ke integer
    exhaustiveness = int(config_variables['exhaustiveness'])  # Konversi ke integer
    num_iterations = 1000
    cpu = os.cpu_count()
    
    size_x = float(config_variables['size_x'])  
    size_y = float(config_variables['size_y'])  
    size_z = float(config_variables['size_z']) 

    print_dev(developer_note, developer_contact, citation_list)
    max_workers = os.cpu_count() - 2 
        
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    for model_dir in model_dirs:
        os.chdir(model_dir)  # Pastikan kembali ke direktori awal sebelum mengubah direktori
        model_dir_name = os.path.basename(model_dir)
        
        # Cari file dengan awalan "rec" untuk receptor dan "lig" untuk reference
        receptor_pdb = next((f for f in os.listdir('.') if f.startswith("rec") and f.endswith(".pdb")), None)
        reference_pdb = next((f for f in os.listdir('.') if f.startswith("lig") and f.endswith(".pdb")), None)
        
        if receptor_pdb and reference_pdb:
            delete_files_except_pdb(receptor_pdb, reference_pdb)
        
            # Buat direktori output untuk setiap model      
            output_model_dir = os.path.join(output_dir, model_dir_name)
            os.makedirs(output_model_dir, exist_ok=True)
            
             # Create energy_summary.csv file     
            csv_path = os.path.join(output_model_dir, f"{model_dir_name}.csv")   
            with open(csv_path, 'w') as csv_file:
                csv_file.write("ligand_id, smiles, vina_score\n")
            
            print(f"Processing {model_dir_name} - Docking and save energy of ligand reference")
            x_center, y_center, z_center, size_x, size_y, size_z = process_reference_vina(receptor_pdb, reference_pdb, output_model_dir, csv_path, size_x, size_y, size_z, num_modes, exhaustiveness, cpu, mgl_directory, max_workers)
            process_ligand_test(model_dir, x_center, y_center, z_center, size_x, size_y, size_z, receptor_pdb, output_model_dir, csv_path, mgl_directory, ligand_dir, max_workers)
            sort_and_add_number(csv_path)
            print(f"Success: {model_dir_name.upper()}")
            os.chdir(current_directory)
    
        elif receptor_pdb is None or reference_pdb is None:
            print(f"Skipping {model_dir_name}: receptor or reference file not found")
            os.chdir(current_directory)
    
    # Print developer's note, contact, and citation listdir
    print_dev(developer_note, developer_contact, citation_list)
       

if __name__ == "__main__":
    current_directory =  (os.path.join(os.getcwd(), "LADOCK_lavina")) 
    if os.path.exists(current_directory):  
        main()
    else:
        print("Your job directory (LADOCK_lavina) is not ready. Please create it using:")
        print("ladock --create lavina") 
