import os
import shutil
import requests
import gzip
from tqdm import tqdm
from multiprocessing import Pool
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from os.path import basename, splitext
from Bio.PDB import PDBParser
from main import *
from functools import partial
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures

from utility import (
    sort_and_add_number,
    download_file_with_retry,
    extract_gz,
    prepare_ligand,
    prepare_receptor,
    run_command,
    convert_to_smiles,
    sort_and_add_number,
    print_dev,
    delete_files_except_pdb,
    
)

def docking_vina(pdbqt_receptor, pdbqt_ligand, pdbqt_output, mgl_directory, ensamble='vina', config='config.txt'):
    run_command(f'{ensamble} --receptor {pdbqt_receptor} --ligand {pdbqt_ligand} --config {config} --out {pdbqt_output}')    
    return

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

def read_energy_and_save_to_csv(output_model_dir, pdbqt_output, csv_path, smiles):    
    vina_output_file = os.path.join(output_model_dir, pdbqt_output)
            
    with open(pdbqt_output, 'r') as vina_output:
        lines = vina_output.readlines()

    energy = None
    for line in lines:
        if line.startswith("REMARK VINA RESULT:"):
            energy = float(line.split()[3])
            break  # Stop reading after the first matching line

    if energy is not None:
        with open(csv_path, 'a') as csv_file:
            csv_file.write(f"{pdbqt_output.replace('output_', '').replace('.pdbqt', '').upper()}, {smiles}, {energy:.3f}\n")
    else:
        print(f"No REMARK VINA RESULT line found in the output of {os.path.basename(pdbqt_output)}")

def process_reference(receptor_pdb, reference_pdb, output_model_dir, csv_path, size_x, size_y, size_z, num_modes, exhaustiveness, cpu, mgl_directory, max_workers):    
    
    # Get ligand's center coordinates
    parser = PDBParser()
    
    structure = parser.get_structure("ligand", reference_pdb)
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
    print("\ttotal threads =", cpu)
    print("\tmax workes =", max_workers)
     
    # Prepare receptor and receptor ligand
    reference_name = os.path.splitext(reference_pdb)[0]
    receptor_name = os.path.splitext(receptor_pdb)[0]
    prepare_ligand(reference_pdb, mgl_directory)
    pdbqt_ligand = f'{reference_name}.pdbqt'
    prepare_receptor(receptor_pdb, mgl_directory)
    pdbqt_receptor = f'{receptor_name}.pdbqt'
    pdbqt_output = f'output_{reference_name}.pdbqt' 

    # Run Vina    
    docking_vina(pdbqt_receptor, pdbqt_ligand, pdbqt_output, mgl_directory) 
    
    # save energy and smiles
    molecule = AllChem.MolFromPDBFile(reference_pdb)
    AllChem.SanitizeMol(molecule)
    smiles = AllChem.MolToSmiles(molecule) 
    read_energy_and_save_to_csv(output_model_dir, pdbqt_output, csv_path, smiles)
    
    # Move files
    os.rename(pdbqt_output, os.path.join(output_model_dir, os.path.basename(pdbqt_output)))
    shutil.copyfile(reference_pdb, os.path.join(output_model_dir, os.path.basename(reference_pdb)))
    return x_center, y_center, z_center, size_x, size_y, size_z

def process_datatest(ligand_pdb, sdf_file, receptor_pdb, output_model_dir, csv_path,  mgl_directory, smiles):      
    receptor_name = os.path.splitext(receptor_pdb)[0]    
    ligand_name = os.path.splitext(ligand_pdb)[0]    
    prepare_ligand(ligand_pdb, mgl_directory)
    pdbqt_receptor = f'{receptor_name}.pdbqt'
    pdbqt_ligand = f'{ligand_name}.pdbqt'
    pdbqt_output = f'output_{ligand_name}.pdbqt'
    docking_vina(pdbqt_receptor, pdbqt_ligand, pdbqt_output, mgl_directory) 
    read_energy_and_save_to_csv(output_model_dir, pdbqt_output, csv_path, smiles)
    os.rename(sdf_file, os.path.join(output_model_dir, os.path.basename(sdf_file)))
    os.remove(pdbqt_ligand)
    os.remove(ligand_pdb)
    os.remove(pdbqt_output)
    
def geometery_optimization(smiles, num_conformers=10, maxIters=100):
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, randomSeed=42)
        lowest_energy = float('inf')
        lowest_energy_conf_id = None

        for conf_id in range(mol.GetNumConformers()):
            initial_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id, ignoreInterfragInteractions=False).CalcEnergy()
            AllChem.UFFOptimizeMolecule(mol, confId=conf_id, maxIters=maxIters)
            optimized_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()
            if optimized_energy < lowest_energy:
                lowest_energy = optimized_energy
                lowest_energy_conf_id = conf_id
                optimized_molecule = mol

        return optimized_molecule

    except Exception as e:
        print(f"Error optimizing geometry for SMILES: {smiles}")
        return None  # Mengembalikan None sebagai penanda bahwa terjadi kesalahan

def process_sdf(sdf_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers):
    with open(sdf_file, 'r') as sdf:
        sdf_content = sdf.read()

    suppl = Chem.SDMolSupplier()
    suppl.SetData(sdf_content)
    
    def process_and_save_data(mol, receptor_pdb, output_model_dir, csv_path, mgl_directory):
    	
        try:
            ligand_name = mol.GetProp("_Name")
            sdf_file_name = f"{ligand_name}.sdf"
            pdb_file_name = f"{ligand_name}.pdb"
            
            smiles = Chem.MolToSmiles(mol)
            Chem.SanitizeMol(mol)
            mol_block = Chem.MolToMolBlock(mol)
            with open(sdf_file_name, 'w') as sdf_file:
                sdf_file.write(mol_block)

            Chem.MolToPDBFile(mol, pdb_file_name)
            
            process_datatest(pdb_file_name, sdf_file_name, receptor_pdb, output_model_dir, csv_path, mgl_directory, smiles)

        except Exception as e:
            pass

    def run_parallel_molecule_processing(suppl, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for _ in tqdm(executor.map(lambda mol: process_and_save_data(mol, receptor_pdb, output_model_dir, csv_path, mgl_directory), suppl),
                          total=len(suppl),
                          desc="Processing sdf molecules",
                          unit="molecule"):
                pass

    run_parallel_molecule_processing(suppl, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers)

def process_smi(smi_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers):
    # Membaca isi file SMILES
    with open(smi_file, 'r') as smi_file:
        smi_content = smi_file.read().splitlines()

    def process_and_save_data(smiles, receptor_pdb, output_model_dir, csv_path, mgl_directory):
        try:
            # Mendapatkan nama ligand dari isi file SMILES
            mol = Chem.MolFromSmiles(smiles)
            
            if mol is not None:
                ligand_name = smiles.strip().split()[1]
                smiles = smiles.strip().split()[0]
                sdf_file_name = f"{ligand_name}.sdf"
                pdb_file_name = f"{ligand_name}.pdb"

                # Melakukan optimasi geometri pada molekul dari SMILES
                mol = geometery_optimization(smiles)  # Perlu didefinisikan

                # Menyimpan molekul dalam format PDB
                Chem.MolToPDBFile(mol, pdb_file_name)

                # Menyimpan molekul dalam format SDF
                mol_block = Chem.MolToMolBlock(mol)
                with open(sdf_file_name, 'w') as sdf_file:
                    sdf_file.write(mol_block)

                # Memproses data uji
                process_datatest(pdb_file_name, sdf_file_name, receptor_pdb, output_model_dir, csv_path, mgl_directory, smiles)

        except Exception as e:
            # Menangani exception, sesuaikan dengan kebutuhan Anda
            # print(f"Error processing SMILES: {smiles}")
            # print(f"Error details: {e}")
            pass

    def run_parallel_molecule_processing(smiles_list, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_and_save_data, smiles, receptor_pdb, output_model_dir, csv_path, mgl_directory): smiles for smiles in smiles_list}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing smiles molecules", unit="molecule"):
                pass

    run_parallel_molecule_processing(smi_content, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers)



def process_ligand_test(model_dir, x_center, y_center, z_center, size_x, size_y, size_z, receptor_pdb, output_model_dir, csv_path, mgl_directory, ligand_dir, max_workers):    
    for ligand_file in os.listdir(ligand_dir):
        if ligand_file.endswith('.txt'):
            file_path = os.path.join(ligand_dir, ligand_file)
            with open(file_path, 'r') as file:
                ligand_links = [line.strip() for line in file.readlines() if 'http' in line and not line.strip().startswith('#')]

            for ligand_link in ligand_links:
                ligand_file_base = basename(ligand_link)
                ligand_name = splitext(ligand_file_base)[0]
                download_file_with_retry(ligand_link, ligand_file_base)
                                    
                if ligand_file_base.endswith('.gz'):
                    try:
                        extract_gz(ligand_file_base)
                        os.remove(ligand_file_base)
                    except Exception as e:
                        continue
                
                smi_files = [f for f in os.listdir('.') if f.endswith(".smi")]
                sdf_files = [f for f in os.listdir('.') if f.endswith(".sdf")]
                
                for smi_file in smi_files:
                    process_smi(smi_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers)
                    os.remove(smi_file)
                    
                for sdf_file in sdf_files:
                    process_sdf(sdf_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers)
                    os.remove(sdf_file) 
                    
        elif any(ligand_file.endswith(ext) for ext in ['.smi', 'smiles']):
            process_smi(ligand_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers)
            os.remove(ligand_file)   
            
        else:
            process_sdf(ligand_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers)
            os.remove(ligand_file)
                 
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

    prepare_gpf = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_gpf4.py")
    prepare_dpf = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_dpf4.py")
    prepare_lowest_energy = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "write_lowest_energy_ligand.py")
    prepare_summarize_result = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "summarize_results4.py")
    pdbqt_to_pdb = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "pdbqt_to_pdb.py")

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
                csv_file.write("ligand_id, smiles, docking_score\n")
            
            print(f"Processing {model_dir_name} - Docking and save energy of ligand reference")
            x_center, y_center, z_center, size_x, size_y, size_z = process_reference(receptor_pdb, reference_pdb, output_model_dir, csv_path, size_x, size_y, size_z, num_modes, exhaustiveness, cpu, mgl_directory, max_workers)
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
