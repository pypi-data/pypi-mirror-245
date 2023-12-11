import os
import sys
import urllib.request
import pandas as pd
from tensorflow import keras
from tqdm import tqdm
from functools import partial
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
from urllib.parse import urlparse
from ladock.PrepareData.calculate_descriptors import get_2d_descriptors, get_3d_descriptors, get_lipinski_descriptors, get_morgan_fp_descriptors, get_maccs_fp_descriptors, get_daylight_fp_descriptors, get_avalon_fp_descriptors, get_tt_fp_descriptors, get_pubchem_fp_descriptors
import numpy as np
import traceback
from os.path import basename
from ladock.ladeepdock.config import lismode, mode_2d, mode_3d, mode_fp
from ladock.utility import print_dev, delete_files_except_pdb, download_file_with_retry 
from ladock.PrepareData.geometry_optimization import optimize_geometry

def using_model(smiles_list, mol_list, mode, model, desired_threads, output_csv):
    # Membuat file CSV jika belum ada
    if not os.path.exists(output_csv):
        with open(output_csv, 'w') as csv_file:
            csv_file.write("lig_id, smiles, deep_score\n")

    def process_smiles(args):
        smiles, mol = args
        lig_id = smiles.strip().split()[1]
        smiles = smiles.strip().split()[0]

        try:
            descriptors = globals()['get_' + mode + '_descriptors'](mol, smiles)
            score = model.predict(np.array([descriptors]))

            result_dict = {'lig_id': lig_id, 'smiles': smiles, 'deep_score': score[0]}
            result_df = pd.DataFrame(result_dict)

            # Menambahkan hasil ke file CSV secara bertahap
            with open(output_csv, 'a') as csv_file:
                result_df.to_csv(csv_file, mode='a', header=False, index=False)

            return output_csv
        except Exception as e:
            print(f"Error processing smiles: {smiles}. Skipping...")
            traceback.print_exc()
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
        args_list = zip(smiles_list, mol_list)
        futures = list(tqdm(executor.map(process_smiles, args_list), total=len(smiles_list), desc="Processing SMILES", unit="molecule"))

    return output_csv

def process_ligand_file(ligand_file, getoutput_dir, lismode, model_output_path, model_dir_name):
    result_df = []
    ligand_name = os.path.basename(ligand_file).upper()

    with open(ligand_file, 'r') as file:
        
        smiles_list = file.read().splitlines()
        
    smiles_list = [line for line in smiles_list if "smiles" not in line.lower()]

    # Get the number of available CPU cores
    total_threads = os.cpu_count()
    desired_threads = max(1, total_threads - 2)

    # Calculation descriptor by modes
    modes = lismode.split(', ')
    mol_list_2d = mol_list_3d = mol_list_fp = None

    if any(mode in modes for mode in mode_2d):
        with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
            input_data = zip(smiles_list, modes * len(smiles_list))
            mol_list_2d = list(tqdm(executor.map(lambda x: optimize_geometry(x), input_data), total=len(smiles_list), desc="Molecules preparation for 2D descriptors", unit="molecule"))
            mol_list_2d = [mol for mol in mol_list_2d if mol is not None]

    if any(mode in modes for mode in mode_3d):
        with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
            input_data = zip(smiles_list, modes * len(smiles_list))
            mol_list_3d = list(tqdm(executor.map(lambda x: optimize_geometry(x), input_data), total=len(smiles_list), desc="Molecules preparation for 3D descriptors", unit="molecule"))
            mol_list_3d = [mol for mol in mol_list_3d if mol is not None]

    if any(mode in modes for mode in mode_fp):
        with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
            input_data = zip(smiles_list, modes * len(smiles_list))
            mol_list_fp = list(tqdm(executor.map(lambda x: optimize_geometry(x), input_data), total=len(smiles_list), desc="Molecules preparation for Fingerprints", unit="molecule"))
            mol_list_fp = [mol for mol in mol_list_fp if mol is not None]

    for mode in modes:
        try:
            output_csv = os.path.join(getoutput_dir, f'{model_dir_name}_{mode}_predicted.csv')           
            model = keras.models.load_model(model_output_path)

            if mode in mode_2d:
                output_csv = using_model(smiles_list, mol_list_2d, mode, model, desired_threads, output_csv)
            if mode in mode_3d:
                output_csv = using_model(smiles_list, mol_list_3d, mode, model, desired_threads, output_csv)
            if mode in mode_fp:
                output_csv = using_model(smiles_list, mol_list_fp, mode, model, desired_threads, output_csv)
                
        except Exception as e:
            print(f"Error in {mode} mode: {e}")

    return output_csv

    
def testing_model(model_output_path, dl_lines, getoutput_dir, mode, model_dir_name):
    result_list = []

    for ligand_link in dl_lines:
        ligand_file_base = os.path.basename(ligand_link)
        ligand_name, ligand_extension = os.path.splitext(ligand_file_base)

        download_file_with_retry(ligand_link, ligand_file_base)

        if ligand_extension == '.gz':
            try:
                extract_gz(ligand_file_base)
            except Exception as e:
                print(f"Error extracting {ligand_file_base}: {e}")
                # Do not remove the file if extraction fails
                continue

            os.remove(ligand_file_base)
            
        ligand_file_path = f"{ligand_name}.smi" if os.path.exists(f"{ligand_name}.smi") else f"{ligand_name}.sdf"
        if not os.path.exists(ligand_file_path):
            print(f"Ligand file {ligand_file_path} not found. Skipping.")
            continue

        output_csv = process_ligand_file(ligand_file_path, getoutput_dir, mode, model_output_path, model_dir_name)
        
    return output_csv
        
