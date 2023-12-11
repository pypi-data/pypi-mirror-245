import os
import subprocess
import glob
import shutil
import urllib.request
from Bio.PDB import PDBParser
from tqdm import tqdm
import argparse
import gzip
import csv
from main import *  
import concurrent.futures
from concurrent.futures import as_completed
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import RDLogger
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import r2_score, mean_absolute_error
from tensorflow.keras import models, layers
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import random

def run_command(command):
    subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def calculate_gridbox_center(structure):
    print(f"  Calculating GridBox Center")    
    model = structure[0]  # Get the first model from the PDB structure
    atoms = model.get_atoms()  # Get the list of atoms in the model
    
    x_sum = y_sum = z_sum = 0.0
    num_atoms = 0
    
    for atom in atoms:
        x, y, z = atom.get_coord()
        x_sum += x
        y_sum += y
        z_sum += z
        num_atoms += 1
    
    x_center = round(x_sum / num_atoms, 3)
    y_center = round(y_sum / num_atoms, 3)
    z_center = round(z_sum / num_atoms, 3)
    
    return x_center, y_center, z_center

def read_energy_and_save_to_csv(counter, output_model_dir, lig_name, csv_path, input_file, category = "vina_score"):    
    vina_output_file = os.path.join(output_model_dir, f"output_{lig_name}.pdbqt")
    smiles = convert_to_smiles(input_file)
        
    with open(vina_output_file, 'r') as vina_output:
        lines = vina_output.readlines()

    energy = None
    for line in lines:
        if line.startswith("REMARK VINA RESULT:"):
            energy = float(line.split()[3])
            break  # Stop reading after the first matching line

    if energy is not None:
        with open(csv_path, 'a') as csv_file:
            csv_file.write(f"{counter['value']}, {lig_name.replace('output_', '').replace('_minimized', '').upper()}, {smiles}, {energy:.3f}, {category}\n")
    else:
        print(f"No REMARK VINA RESULT line found in the output of {os.path.basename(lig_pdbqt_path)}")

def process_docking_ligand_native(counter, size_x, size_y, size_z, num_modes, exhaustiveness, max_workers, num_iterations, csv_path, prepare_receptor, receptor_name, prepare_ligand, lig_name, directory, ensamble, output_model_dir, cpu):

    # Get ligand's center coordinates
    parser = PDBParser()
    lig_pdb_path = os.path.join(current_directory, directory, f"{lig_name}.pdb")

    structure = parser.get_structure("ligand", lig_pdb_path)
    x_center, y_center, z_center = calculate_gridbox_center(structure)

    # Create config.txt with updated values
    with open('config.txt', 'w') as config_file:
        config_file.write(f"size_x = {size_x}\n")
        config_file.write(f"size_y = {size_y}\n")
        config_file.write(f"size_z = {size_z}\n")
        config_file.write(f"center_x = {x_center}\n")
        config_file.write(f"center_y = {y_center}\n")
        config_file.write(f"center_z = {z_center}\n")
        config_file.write(f"num_modes = {num_modes}\n")
        config_file.write(f"exhaustiveness = {exhaustiveness}\n")
        config_file.write(f"cpu = {cpu}\n")
        config_file.write("# Script written by:\n")
        config_file.write("# La Ode Aman\n")
        config_file.write("# laodeaman.ai@gmail.com\n")
        config_file.write("# laode_aman@ung.ac.id\n")
        config_file.write("# Universitas Negeri Gorontalo, Indonesia\n")

    print("  Docking parameter:")
    print("\tsize_x =", size_x)
    print("\tsize_y =", size_y)
    print("\tsize_z =", size_z)
    print("\tcenter_x =", x_center)
    print("\tcenter_y =", y_center)
    print("\tcenter_z =", z_center)
    print("\tnum_modes =", num_modes)
    print("\texhaustiveness =", exhaustiveness)
    print("\tcpu =", cpu)

    # Create energy_summary.csv
     
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as csv_file:
            csv_file.write("No, LigandName, canonical_smiles, score, category\n")
    else:
        pass
      
    # Prepare receptor and native ligand
    run_command(f'{prepare_receptor} -r {receptor_name}.pdb')
    run_command(f'{prepare_ligand} -l {lig_name}.pdb')
    input_file = f'{lig_name}.pdb'    
    
    # Run Vina
    print(f"  Docking and save energy")
    run_command(f'{ensamble} --receptor {receptor_name}.pdbqt --ligand {lig_name}.pdbqt --config config.txt --out output_{lig_name}.pdbqt')


    # Move files
    os.rename(f"output_{lig_name}.pdbqt", os.path.join(output_model_dir, f"output_{lig_name}.pdbqt"))
    
    # Save to csv   
    read_energy_and_save_to_csv(counter, output_model_dir, lig_name, csv_path, input_file)
         
def process_and_optimize_smi(prepare_ligand, smi_file, ligand_tmp_dir):
    try:
        with open(smi_file, 'r') as file:
            parts = file.readline().split()[1]
            file_name = parts.split('/')[-1]
            new_name = file_name.split('.')[0].upper()

        # Convert .smi to .mol
        obabel_convert_command_mol = f'obabel {smi_file} -omol -h -O {new_name}.mol --gen2d'
        subprocess.run(obabel_convert_command_mol, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Perform geometry optimization (output: .pdb)
        obminimize_input = f"{new_name}.mol"
        obminimize_output = f"{new_name}_minimized.pdb"
        obminimize_command = f'obminimize -o "pdb" {obminimize_input} > {obminimize_output}'
        subprocess.run(obminimize_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        convert_to_pdbqt(obminimize_output, prepare_ligand)
        os.remove(smi_file)
        os.remove(obminimize_input)
        os.remove(obminimize_output)
    except subprocess.CalledProcessError as e:
        pass
       
def process_in_ligand_tmp_dir(prepare_ligand, ligand_tmp_file, ligand_tmp_dir, max_workers):
    os.chdir(ligand_tmp_dir)
    smi_futures = []
    sdf_futures = []
    smi_files = [f for f in os.listdir(ligand_tmp_dir) if f.endswith(".smi")]
         
    if smi_files:  # Periksa apakah ada file .smi yang tersedia
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                for smi_file in smi_files:
                    smi_futures.append(executor.submit(process_and_optimize_smi, prepare_ligand, smi_file, ligand_tmp_dir))
                
                for future in tqdm(concurrent.futures.as_completed(smi_futures), total=len(smi_futures), desc="  Geometry optimization"):
                    try:
                        future.result()
                    except Exception as e:
                        pass
    
def process_ligand_link_DL(ligand_url, ligand_dir, ligand_tmp_dir, lig_name, num_iterations, max_workers, size_x, size_y, size_z, num_modes, exhaustiveness, csv_path, prepare_receptor, receptor_name, prepare_ligand, directory, ensamble, output_model_dir, counter, cpu):
    retry_count = 0
    max_retries = 10
    ligand_file = None  # Inisialisasi variabel ligand_file
    
    while retry_count < max_retries:
        try:
            # Download the ligand file
            ligand_file = os.path.join(ligand_dir, os.path.basename(ligand_url))
            urllib.request.urlretrieve(ligand_url, ligand_file)
            
            break
            
        except Exception as e:
            print(e)
            print(f"Retrying to download: {ligand_url}")
            retry_count += 1

    if retry_count == max_retries:
        print(f"Failed to download ligand after {max_retries} retries.")
    
    if ligand_file and ligand_file.endswith(".gz"):
        # Extract the .gz file
        extracted_file = os.path.splitext(ligand_file)[0]  # Remove .gz extension
        with gzip.open(ligand_file, 'rb') as gz_file, open(extracted_file, 'wb') as out_file:
            out_file.writelines(gz_file)
        
        # Remove the downloaded .gz file
        os.remove(ligand_file)
        
        # Update the ligand_file to the extracted file
        ligand_file = extracted_file
    
    # Read all lines into a list
    with open(ligand_file, 'r') as file:
        smiles_list = file.readlines()
    
def process_ligand_link(ligand_url, ligand_dir, ligand_tmp_dir, lig_name, num_iterations, max_workers, size_x, size_y, size_z, num_modes, exhaustiveness, csv_path, prepare_receptor, receptor_name, prepare_ligand, directory, ensamble, output_model_dir, counter, cpu):
    retry_count = 0
    max_retries = 10
    ligand_file = None  # Inisialisasi variabel ligand_file
    
    while retry_count < max_retries:
        try:
            # Download the ligand file
            ligand_file = os.path.join(ligand_dir, os.path.basename(ligand_url))
            urllib.request.urlretrieve(ligand_url, ligand_file)
            
            break
            
        except Exception as e:
            print(e)
            print(f"Retrying to download: {ligand_url}")
            retry_count += 1

    if retry_count == max_retries:
        print(f"Failed to download ligand after {max_retries} retries.")
    
    if ligand_file and ligand_file.endswith(".gz"):
        # Extract the .gz file
        extracted_file = os.path.splitext(ligand_file)[0]  # Remove .gz extension
        with gzip.open(ligand_file, 'rb') as gz_file, open(extracted_file, 'wb') as out_file:
            out_file.writelines(gz_file)
        
        # Remove the downloaded .gz file
        os.remove(ligand_file)
        
        # Update the ligand_file to the extracted file
        ligand_file = extracted_file
    
    # Read all lines into a list
    with open(ligand_file, 'r') as file:
        lines = file.readlines()
    
    # Write back the content to the file, excluding the first line
    with open(ligand_file, 'w') as file:
        file.writelines(lines[0:])
    
    if ligand_file.endswith(".smi"):
        preparing_smi_file(ligand_file)
    process_in_ligand_dir(ligand_file, ligand_dir, ligand_tmp_dir)            
    
    # Remove the downloaded ligand file
    os.remove(ligand_file)
    
    valid_extensions = (".sdf", ".smi")
    ligand_tmp_files = [f for f in os.listdir(ligand_tmp_dir) if any(f.endswith(ext) for ext in valid_extensions)]
    num_ligand_files = len(ligand_tmp_files)

    print(f"  Total molecules = {num_ligand_files}")                    
    print(f"  Using {lig_name}.pdb docking parameter as reference")
    
    for ligand_tmp_file in ligand_tmp_files:
        process_in_ligand_tmp_dir(prepare_ligand, ligand_tmp_file, ligand_tmp_dir, max_workers)        
        process_docking_ligand_test(ligand_tmp_dir, counter, size_x, size_y, size_z, num_modes, exhaustiveness, num_iterations, csv_path, prepare_receptor, receptor_name, prepare_ligand, lig_name, directory, ensamble, output_model_dir, cpu)

def convert_to_smiles(input_file):
    """
    Konversi file PDB atau PDBQT menjadi SMILES menggunakan Open Babel.

    Args:
      input_file: Path ke file PDB atau PDBQT.

    Returns:
      SMILES string dari struktur molekul dalam file, atau None jika konversi gagal.
    """
    try:
        output_file = "hasil.smiles"
        obabel_command = f'obabel {input_file} -osmi -O {output_file}'
        subprocess.run(obabel_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        with open(output_file, 'r') as smiles_file:
            smiles = smiles_file.read().strip()

        # Hapus file output setelah mendapatkan SMILES
        os.remove(output_file)

        # Memisahkan SMILES dari nama model jika ada
        smiles = smiles.split('\t')[0]
        return smiles
    except Exception as e:        
        return None

def preparing_smi_file(smi_file_path):
  """Membaca dan menyimpan kembali file .smi yang hanya berisi baris-baris yang valid."""

  # Membaca file .smi ke dalam list
  with open(smi_file_path, 'r') as file:
    lines = file.readlines()

  # Membuat list untuk menyimpan baris-baris yang valid
  valid_lines = []

  for line in lines:
    try:
      mol = Chem.MolFromSmiles(line.strip())
      if mol is not None:
        valid_lines.append(line)
    except:      
      pass

  # Menyimpan kembali file .smi yang hanya berisi baris-baris yang valid
  with open(smi_file_path, 'w') as file:
    file.writelines(valid_lines)

def convert_to_pdbqt(pdb_file, prepare_ligand):
    filename = os.path.splitext(os.path.basename(pdb_file))[0]
    pdbqt_file = f"{filename}.pdbqt"
    run_command(f'{prepare_ligand} -l {pdb_file}')
    return pdbqt_file

def process_in_ligand_dir(ligand_file, ligand_dir, ligand_tmp_dir):    
    os.chdir(ligand_dir)
    ligand_name = os.path.basename(ligand_file)
    print(f"\n  Ligand: {ligand_name}")
    print(f"  Splitting {ligand_name} to single molecule")

    ligand_test = os.path.splitext(os.path.basename(ligand_file))[0]
    try:
        if ligand_file.endswith((".smiles", ".smi")):
            preparing_smi_file(ligand_file)            
            command = f"obabel {ligand_file} -osmi -O {os.path.join(ligand_tmp_dir, ligand_test)}.smi -m -h"
        else:
            return  # Skip unsupported file formats

        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while preparing ligand: {ligand_file}")

def process_docking_ligand(pdbqt_file, counter, prepare_ligand, receptor_name, ensamble, output_model_dir, csv_path):
    try:
        # preparing, docking and save energy        
        filename = os.path.splitext(os.path.basename(pdbqt_file))[0]      
        output_file = os.path.join(output_model_dir, f'output_{filename}.pdbqt')
        run_command(f'{ensamble} --receptor {receptor_name}.pdbqt --ligand {pdbqt_file} --config config.txt --out {output_file}')        
        read_energy_and_save_to_csv(counter, output_model_dir, filename, csv_path, pdbqt_file) 
        os.remove(pdbqt_file)
    except Exception as e:
        print(f"An error occurred while processing a ligand: {e}")

def process_docking_ligand_test(ligand_tmp_dir, counter, size_x, size_y, size_z, num_modes, exhaustiveness, num_iterations, csv_path, prepare_receptor, receptor_name, prepare_ligand, lig_name, directory, ensamble, output_model_dir, max_workers):
    os.chdir(directory)
    ligand_files = glob.glob(os.path.join(ligand_tmp_dir, '*.pdbqt'))
    num_ligand_files = len(ligand_files)
    
    counter ["value"] += 1
    if num_ligand_files == 0:        
        return

    futures = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for pdbqt_file in ligand_files:
            futures.append(executor.submit(
                process_docking_ligand, pdbqt_file, counter, prepare_ligand, receptor_name, ensamble, output_model_dir, csv_path))

        # Gunakan as_completed untuk mengawasi pemrosesan 
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="  Docking and save energy"):
            try:
                future.result()  # Menunggu dan memeriksa hasil tugas (tidak ada yang diabaikan)
            except Exception as e:
                print(f"An error occurred while processing a .sdf file: {e}")

def sort_and_rewrite_csv(csv_path):
    try:
        data = []
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Baca header (baris pertama)
            for row in csv_reader:
                data.append(row)

        # Filter baris dengan kolom SMILES yang kosong atau None        
        data = [row for row in data if row[2] and row[2].strip() != 'None' and row[2].strip() != '']

        # Mengurutkan data berdasarkan kolom keempat (Binding Affinity)
        sorted_data = sorted(data, key=lambda x: float(x[3]))  # Menggunakan lambda untuk mengakses kolom keempat (indeks 3) sebagai kunci pengurutan

        # Menulis data yang sudah diurutkan kembali ke file CSV
        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)            
            csv_file.write("No, LigandName, canonical_smiles, score, category\n")
            for index, row in enumerate(sorted_data, start=1):
                csv_writer.writerow([index] + row[1:])  # Menulis nomor urutan, nama, dan binding affinity

        print(f"Output CSV file is in the {csv_path}")                
        return True
    except Exception as e:
        print(f"Error while sorting and rewriting CSV: {e}")
        return False

def print_dev(developer_note, developer_contact, citation_list):
    print("")
    print(developer_note)
    print("")
    print(developer_contact)
    print("")
    print(citation_list)
    print("")

# Fungsi untuk memuat model DL dari file
def load_docking_model(model_path):
    model = keras.models.load_model(model_path)
    return model

# Fungsi untuk melakukan perhitungan docking score menggunakan model DL
def predict_docking_score(model, molecular_features):
    # Pastikan bahwa molecular_features adalah array numpy yang sesuai dengan input model
    molecular_features = np.array(molecular_features)
    
    # Lakukan prediksi docking score menggunakan model
    docking_score = model.predict(molecular_features)
    
    # Kembalikan hasil prediksi docking score
    return docking_score

def get_2d_descriptors(smiles, missing_val=None):
    mol = Chem.MolFromSmiles(smiles)
    res = {}

    for nm, fn in Descriptors.descList:
        try:
            val = fn(mol)
            print(f"Calculating 2D descriptors {nm} for: {smiles}")
        except Exception as e:
            print(f"Error calculating descriptor {nm} for: {smiles}")
            val = missing_val
        res[nm] = val
    return res

def get_lipinski_descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    descriptors_lipinski = {}

    try:
        descriptors_lipinski['FractionCSP3'] = Lipinski.FractionCSP3(mol)
        # ... (other Lipinski descriptors)

        for desc_name, desc_value in descriptors_lipinski.items():
            print(f"Calculating Lipinski descriptor {desc_name} for: {smiles} - Value: {desc_value}")

    except Exception as e:
        for desc_name in descriptors_lipinski.keys():
            print(f"Error calculating Lipinski descriptor {desc_name} for: {smiles}")
            descriptors_lipinski[desc_name] = None

    return descriptors_lipinski

def get_3d_descriptors(smiles):
    descriptors_3d = {}
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)

    try:
        descriptors_3d = CalcMolDescriptors3D(mol)
        for desc_name, desc_value in descriptors_3d.items():
            print(f"Calculating 3D descriptor {desc_name} for: {smiles} - Value: {desc_value}")

    except Exception as e:
        print(f"Error calculating 3D descriptors for: {smiles}")
        descriptors_3d = {}
    return descriptors_3d

def calculate_descriptors(smiles):
    descriptors = {}
    if smiles is None:
        return None

    descriptors_2d = get_2d_descriptors(smiles, missing_val=None)
    descriptors.update(descriptors_2d)
    descriptors_3d = get_3d_descriptors(smiles)
    descriptors.update(descriptors_3d)
    descriptors_lipinski = get_lipinski_descriptors(smiles)
    descriptors.update(descriptors_lipinski)

    return descriptors

def build_model(input_shape):
    df = pd.read_csv(csv_path)
    smiles_list = df['canonical_smiles'].tolist()
    total_threads = os.cpu_count()
    desired_threads = max(1, total_threads - 2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=desired_threads) as executor:
        results = list(tqdm(executor.map(calculate_descriptors, smiles_list), total=len(smiles_list)))

    df_descriptor = pd.DataFrame(results)
    df_combined = pd.concat([df, df_descriptor], axis=1)
    df_combined = df_combined.loc[:, ~df_combined.columns.duplicated()]

    df = df_combined
    df = df.dropna()

    y = df['docking_score']
    X_features = df.drop(columns=['No', 'LigandName', 'canonical_smiles', 'score', 'category'], axis=1)

    scaler_X = StandardScaler()
    scaler_y = RobustScaler()
    X_normalized = scaler_X.fit_transform(X_features)
    y_normalized = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

    num_rows, num_columns = X_features.shape
    print("Number of Rows:", num_rows)
    print("Number of Columns:", num_columns)

    feature_list = X_features.columns
    feature_indices = [X_features.columns.get_loc(feature) for feature in feature_list]
    X_train, X_test, y_train, y_test = train_test_split(X_normalized[:, feature_indices], y_normalized, test_size=0.2, random_state=1)

    y_train_original_scale = scaler_y.inverse_transform(y_train.reshape(-1, 1)).flatten()
    y_test_original_scale = scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()

    model = models.Sequential()
    model.add(layers.Conv3D(32, (3, 3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling3D((2, 2, 2)))
    model.add(layers.Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(layers.MaxPooling3D((2, 2, 2)))
    model.add(layers.Conv3D(128, (3, 3, 3), activation='relu'))
    model.add(layers.MaxPooling3D((2, 2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    callback = EarlyStopping(monitor='val_loss', patience=100, verbose=1)

    history = model.fit(X_train, y_train, epochs=100, batch_size=128, validation_data=(X_test, y_test), callbacks=[callback])

    y_pred = model.predict(X_test)
    y_pred_original_scale = scaler_y.inverse_transform(y_pred.reshape(-1, 1)).flatten()

    y_train_pred = model.predict(X_train)
    y_train_pred_original_scale = scaler_y.inverse_transform(y_train_pred.reshape(-1, 1)).flatten()

    plt.scatter(y_test_original_scale, y_pred_original_scale, alpha=0.5, label=f'Validation Data: {len(X_test)} molecules')
    plt.scatter(y_train_original_scale, y_train_pred_original_scale, alpha=0.5, label=f'Train Data: {len(X_train)} molecules')

    plt.xlabel('True pIC50')
    plt.ylabel('Predicted pIC50')

    plt.xlim(0, 14)
    plt.ylim(0, 14)

    z_test = np.polyfit(y_test_original_scale, y_pred_original_scale, 1)
    p_test = np.poly1d(z_test)
    z_train = np.polyfit(y_train_original_scale, y_train_pred_original_scale, 1)
    p_train = np.poly1d(z_train)

    r2_test = r2_score(y_test_original_scale, y_pred_original_scale)
    r2_train = r2_score(y_train_original_scale, y_train_pred_original_scale)

    mae_test = mean_absolute_error(y_test_original_scale, y_pred_original_scale)
 
def predict_docking_score(model, X_features, smiles, df):
    # Convert X_features to a numpy array
    molecular_features = np.array(X_features)

    # Predict docking score using the model and molecular features
    docking_score = model.predict(molecular_features)

    # Add docking_score to the dataframe (assuming df is a Pandas DataFrame)
    df['canonical_smiles'] = smiles
    df['DL_score'] = docking_score

    return df


def main(): 
    print_dev(developer_note, developer_contact, citation_list)
    
    os.chdir(current_directory)
    config_file = 'config_lavinadl.txt'
    
    with open(config_file, 'r') as config_file:
        config_lines = config_file.readlines()
    
    config_variables = {}
    retry_count = 0
    
    for line in config_lines:
        if not line.strip().startswith('#'):
            try:
                name, value = line.strip().split('=')
                name = name.strip()
                value = value.strip()
                config_variables[name] = value
            except ValueError:
                pass

    ensamble = vina  # Ganti "vina" dengan string yang sesuai
    num_modes = int(config_variables['num_modes'])  # Konversi ke integer
    exhaustiveness = int(config_variables['exhaustiveness'])  # Konversi ke integer
    num_iterations = 1000
    cpu = os.cpu_count()
    max_workers = os.cpu_count()
    
    size_x = float(config_variables['size_x'])  
    size_y = float(config_variables['size_y'])  
    size_z = float(config_variables['size_z'])  
    ligand_dir = os.path.join(current_directory, 'ligand_input')
    ligand_tmp_dir = os.path.join(current_directory, 'ligand_tmp')
    output_dir = os.path.join(current_directory, 'output')
    
    mgl_directory = config_variables['mgl_directory']
    prepare_ligand = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_ligand4.py")    
    prepare_receptor = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_receptor4.py")
    prepare_gpf = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_gpf4.py")
    prepare_dpf = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_dpf4.py")
    prepare_lowest_energy = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "write_lowest_energy_ligand.py")
    prepare_summarize_result = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "summarize_results4.py")
    
    print("Removing unnecessary files and directories in job directory...")

    # Create ligand_tmp and output directory if it doesn't exist
    if os.path.exists(ligand_tmp_dir):
        shutil.rmtree(ligand_tmp_dir)
    os.makedirs(ligand_tmp_dir, exist_ok=True)    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)     
   
    for directory in os.listdir(current_directory):
        if os.path.isdir(directory):
            counter = {"value": 0}
            dir_name = os.path.basename(directory)
            receptor_name = ""
            lig_name = ""
            print(f"\nProcessing {dir_name.upper()}")
            os.chdir(directory)
            receptor_files = glob.glob('rec*.pdb')
            if receptor_files:    
                receptor_name = os.path.splitext(os.path.basename(receptor_files[0]))[0]
            ligand_files = glob.glob('lig*.pdb')
            if ligand_files:    
                lig_name = os.path.splitext(os.path.basename(ligand_files[0]))[0]                
            output_model_dir = os.path.join(output_dir, dir_name)         
            os.makedirs(output_model_dir, exist_ok=True)
            csv_path = os.path.join(output_model_dir, 'energy_summary.csv')
                
            if os.path.exists(f"{receptor_name}.pdb") and os.path.exists(f"{lig_name}.pdb"):
                with open(csv_path, 'w') as csv_file:
                    csv_file.write("No, LigandName, canonical_smiles, score, category\n")
                print("Docking reference ligand:")
                print(f"  Receptor: {receptor_name}.pdbqt")
                print(f"  Ligand: {lig_name}.pdbqt")
                process_docking_ligand_native(counter, size_x, size_y, size_z, num_modes, exhaustiveness, max_workers, num_iterations, csv_path, prepare_receptor, receptor_name, prepare_ligand, lig_name, directory, ensamble, output_model_dir, cpu)
                print("\nDocking test ligands: ")
                print(f"  Receptor: {receptor_name}.pdbqt")                  
                os.chdir(ligand_dir)
                
                valid_extensions = (".txt")
                ligand_link_files = [f for f in os.listdir(ligand_dir) if any(f.endswith(ext) for ext in valid_extensions)]
                
                # Iterasi melalui file ligand_link
                for ligand_link_path in ligand_link_files:
                    if os.path.exists(ligand_link_path):
                        with open(ligand_link_path, 'r') as f:
                            lines = f.readlines()



                        # Iterasi melalui ligand_link_files
                        for ligand_link_path in ligand_link_files:
                            if os.path.exists(ligand_link_path):
                                with open(ligand_link_path, 'r') as f:
                                    lines = f.readlines()

                                # Hapus baris yang tidak valid dan yang dimulai dengan "#"
                                valid_lines = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

                                # Ambil 10% dari lines secara acak
                                random.shuffle(valid_lines)
                                vina_lines = valid_lines[:int(0.005 * len(valid_lines))]

                                # Convert valid_lines and vina_lines to sets
                                valid_lines_set = set(valid_lines)
                                vina_lines_set = set(vina_lines)

                                # Perform set subtraction
                                dl_lines_set = valid_lines_set - vina_lines_set

                                # Convert dl_lines_set back to a list if needed
                                dl_lines = list(dl_lines_set)

                                # Iterasi melalui vina_lines
                                for line in vina_lines:
                                    ligand_url = line.strip()
                                    process_ligand_link(ligand_url, ligand_dir, ligand_tmp_dir, lig_name, num_iterations, max_workers, size_x, size_y, size_z, num_modes, exhaustiveness, csv_path, prepare_receptor, receptor_name, prepare_ligand, directory, ensamble, output_model_dir, counter, cpu)
                                sort_and_rewrite_csv(csv_path)                                 
                                model = build_model() 

                                # Iterasi melalui dl_lines
                                for line in dl_lines:
                                    ligand_url = line.strip()
                                    smiles_list = process_ligand_link_DL(ligand_url, ligand_dir, ligand_tmp_dir, lig_name, num_iterations, max_workers, size_x, size_y, size_z, num_modes, exhaustiveness, csv_path, prepare_receptor, receptor_name, prepare_ligand, directory, ensamble, output_model_dir, counter, cpu)
                                    for smiles in smiles_list:
                                        predict_docking_score(model, X_features, smiles, df)
                
                print(f"Success: {dir_name.upper()}")

            else:
                print(f"Skipping docking: receptor or reference ligand in {dir_name} not found.")
                os.chdir(current_directory) 

    # Print developer's note, contact, and citation listdir
    print_dev(developer_note, developer_contact, citation_list)

if __name__ == "__main__":
    current_directory =  (os.path.join(os.getcwd(), "LADOCK_lavinadl")) 
    if os.path.exists(current_directory):  
        main() 
    else:
        print("Your job directory (LADOCK_lavinadl) is not ready. Please create it using:")
        print("ladock --create lavinadl")
