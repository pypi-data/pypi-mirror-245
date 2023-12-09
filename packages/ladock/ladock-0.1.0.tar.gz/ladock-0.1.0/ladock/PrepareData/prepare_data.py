import os
import pandas as pd
import concurrent.futures
from tqdm import tqdm
from calculate_descriptors import get_2d_descriptors, get_3d_descriptors, get_lipinski_descriptors, get_morgan_fp_descriptors, get_maccs_fp_descriptors, get_daylight_fp_descriptors, get_avalon_fp_descriptors, get_tt_fp_descriptors, get_pubchem_fp_descriptors
import time
from rdkit import Chem
from rdkit.Chem import AllChem
from geometry_optimization import optimize_geometry
from config import lismode, mode_2d, mode_3d, mode_fp, input_column
from concurrent.futures import ThreadPoolExecutor  # or ProcessPoolExecutor

def calculate_and_save_descriptors(total_threads, df, descriptor_function, mol_list, smiles_list, output_file, mode, desired_threads):
    start_time = time.time()
    descriptor_type = mode.upper()
    print(f"\nDescriptors calculation for {mode}...")    
    # Descriptors calculation    
    with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
        results = list(tqdm(executor.map(descriptor_function, mol_list, smiles_list), total=len(mol_list)))
    # Create DataFrames
    df_descriptor = pd.DataFrame(results)
    df_combined = pd.concat([df, df_descriptor], axis=1)
    df_combined = df_combined.loc[:, ~df_combined.columns.duplicated()]
    df_combined = df_combined.dropna()

    # Save DataFrame to CSV
    df_combined.to_csv(output_file, index=False)
    print(df_combined)

    # Print the values
    print("\nUsing", desired_threads, "of", total_threads, "cpu")
    end_time = time.time()
    total_execution_time = end_time - start_time
    print(f"Calculation time of {descriptor_type} descriptors: {total_execution_time:.2f} seconds")

def prepareData(csv_file, input_dir, output_dir):
   
    # Mendapatkan nama berkas tanpa ekstensi
    fn_csv = os.path.splitext(os.path.basename(csv_file))[0]

    # Membuat direktori output jika belum ada
    output_subdir = os.path.join(output_dir, fn_csv)
    os.makedirs(output_subdir, exist_ok=True)

    # Menyiapkan path untuk input dan output
    input_csv = os.path.join(input_dir, csv_file)
    
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()
    # df = df.head()
    
    # Mencari nama kolom yang cocok dengan keyword
    matching_columns = [col for col in df.columns if input_column.lower() in col.lower()]

    # Memeriksa apakah ada kolom yang cocok
    if matching_columns:
        # Menggunakan kolom pertama yang cocok
        selected_column = matching_columns[0]
        smiles_list = df[selected_column].tolist()

    # Get the number of available CPU cores
    total_threads = os.cpu_count()
    desired_threads = max(1, total_threads - 2)

    # Calculation descriptor by modes
    modes = lismode.split(', ')

    mol_list_2d = mol_list_3d = mol_list_fp = None  

    # Check for 2D mode
    if any(mode in modes for mode in mode_2d):
        print("\nMolecules preparation for 2D descriptors...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
            d2_modes = [mode for mode in modes if mode in mode_2d]
            input_data = zip(smiles_list, d2_modes * len(smiles_list))
            mol_list_2d = list(tqdm(executor.map(lambda x: optimize_geometry(x), input_data), total=len(smiles_list)))
            mol_list_2d = [mol for mol in mol_list_2d if mol is not None]

    # Check for 3D mode
    if any(mode in modes for mode in mode_3d):
        print("\nMolecules preparation for 3D descriptors...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
            d3_modes = [mode for mode in modes if mode in mode_3d]
            input_data = zip(smiles_list, d3_modes * len(smiles_list))
            mol_list_3d = list(tqdm(executor.map(lambda x: optimize_geometry(x), input_data), total=len(smiles_list)))
            mol_list_3d = [mol for mol in mol_list_3d if mol is not None]

    # Check for FP mode
    if any(mode in modes for mode in mode_fp):
        print("\nMolecules preparation for FP descriptors...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
            fp_modes = [mode for mode in modes if mode in mode_fp]
            input_data = zip(smiles_list, fp_modes * len(smiles_list))
            mol_list_fp = list(tqdm(executor.map(lambda x: optimize_geometry(x), input_data), total=len(smiles_list)))
            mol_list_fp = [mol for mol in mol_list_fp if mol is not None]

    for mode in modes:
        descriptor_function = f'get_{mode}_descriptors'
        output_file = os.path.join(output_subdir, f'{fn_csv}_{mode}.csv')
        descriptor_function = globals()[descriptor_function]
        try:
            if mode in mode_2d:
                calculate_and_save_descriptors(total_threads, df, descriptor_function, mol_list_2d, smiles_list, output_file, mode, desired_threads)
            elif mode in mode_3d:      
                calculate_and_save_descriptors(total_threads, df, descriptor_function, mol_list_3d, smiles_list, output_file, mode, desired_threads)
            elif mode in mode_fp:
                calculate_and_save_descriptors(total_threads, df, descriptor_function, mol_list_fp, smiles_list, output_file, mode, desired_threads)
            
        except Exception as e:
            print(f"Error in {mode} mode: {e}")
