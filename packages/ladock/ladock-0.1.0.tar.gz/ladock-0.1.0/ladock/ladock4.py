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

def read_energy_and_save_to_csv(output_file, csv_path, lig_name, smiles):
    # Buka file untuk membaca    
    with open(output_file, 'r') as file:
        content = file.read()

    # Cari baris yang mengandung "RMSD TABLE"
    in_rmsd_table = False
    for line in content.split('\n'):
        if "RMSD TABLE" in line:
            in_rmsd_table = True
            continue
        if in_rmsd_table:
            if line.strip():
                words = line.split()
                try:
                    energy = float(words[3])
                    break
                except (ValueError, IndexError):
                    pass
    else:
        print("Tabel RMSD tidak ditemukan atau tidak ada nilai energy pada baris pertama kolom keempat.")

    # Jika energy ditemukan, simpan ke dalam CSV
    if energy is not None:
        with open(csv_path, 'a') as csv_file:
            csv_file.write(f"{lig_name.replace('_minimized', '').upper()}, {smiles}, {energy:.3f}\n")
            

def process_reference(prepare_gpf, prepare_dpf, spacing, npts, max_workers, csv_path, prepare_receptor, prepare_ligand, ensamble, output_model_dir, parameter, receptor_pdb, reference_pdb):

    # Create energy_summary.csv
    print("  Docking and save energy ...")
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as csv_file:
            csv_file.write("No., Ligand ID (name), canonical_smiles, Binding Affinity (kcal per mol)\n")
    else:
        pass
   
    # Prepare receptor & native, gpf, autogrid4, dpf, autodock4
    lig_name = os.path.splitext(os.path.basename(reference_pdb))[0]
    receptor_name = os.path.splitext(os.path.basename(receptor_pdb))[0]
    output_file = os.path.join(output_model_dir, f"output_{lig_name}.dlg")
    input_file = reference_pdb
    
    run_command(f'{prepare_ligand} -l {lig_name}.pdb')    
    run_command(f'{prepare_receptor} -r {receptor_name}.pdb -o {lig_name}_{receptor_name}.pdbqt -A checkhydrogens') 
    run_command(f'{prepare_gpf} -l {lig_name}.pdbqt -r {lig_name}_{receptor_name}.pdbqt -y -o {lig_name}_{receptor_name}.gpf')
    run_command(f'autogrid4 -p {lig_name}_{receptor_name}.gpf -l {lig_name}_{receptor_name}.glg')
    run_command(f'{prepare_dpf} -l {lig_name}.pdbqt -r {lig_name}_{receptor_name}.pdbqt {parameter} -o {lig_name}_{receptor_name}.dpf')
    run_command(f'{ensamble} -p {lig_name}_{receptor_name}.dpf -l {output_file}')  

    # save energy and smiles
    molecule = AllChem.MolFromPDBFile(reference_pdb)
    AllChem.SanitizeMol(molecule)
    smiles = AllChem.MolToSmiles(molecule) 
    read_energy_and_save_to_csv(output_file, csv_path, lig_name, smiles)
    shutil.copyfile(reference_pdb, os.path.join(output_model_dir, os.path.basename(reference_pdb)))

def process_datatest(prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, pdb_file, sdf_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, smiles, reference_pdb, parameter, ensamble):
    try:
        filename = os.path.splitext(os.path.basename(pdb_file))[0]
        lig_name = os.path.splitext(os.path.basename(reference_pdb))[0]
        receptor_name = os.path.splitext(os.path.basename(receptor_pdb))[0]
        output_file = os.path.join(output_model_dir, f'output_{filename}.dlg')
        dest_path = os.path.join(".", filename + ".pdbqt")     
        input_file = f'{filename}.pdbqt'
       
        # Prepare receptor & native, gpf, autogrid4, dpf, autodock4
        run_command(f'{prepare_ligand} -l {filename}.pdb')
        run_command(f'{prepare_receptor} -r {receptor_name}.pdb -o {filename}_{receptor_name}.pdbqt -A checkhydrogens') 
        run_command(f'{prepare_gpf} -l {filename}.pdbqt -r {filename}_{receptor_name}.pdbqt -i {lig_name}_{receptor_name}.gpf -o {filename}_{receptor_name}.gpf')
        run_command(f'autogrid4 -p {filename}_{receptor_name}.gpf -l {filename}_{receptor_name}.glg')
        run_command(f'{prepare_dpf} -l {filename}.pdbqt -r {filename}_{receptor_name}.pdbqt {parameter} -i {lig_name}_{receptor_name}.dpf -o {filename}_{receptor_name}.dpf')
        run_command(f'{ensamble} -p {filename}_{receptor_name}.dpf -l {output_file}')
        read_energy_and_save_to_csv(output_file, csv_path, filename, smiles)
        os.remove(output_file)
        os.rename(sdf_file, os.path.join(output_model_dir, os.path.basename(sdf_file)))  
      
        # Remove the original and intermediate files
        file_to_remove = glob.glob(f'{filename}*')
        for file in file_to_remove:
            os.remove(file)

            
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")
    
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

def process_sdf(sdf_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble):
    with open(sdf_file, 'r') as sdf:
        sdf_content = sdf.read()

    suppl = Chem.SDMolSupplier()
    suppl.SetData(sdf_content)
    
    def process_and_save_data(mol, receptor_pdb, output_model_dir, csv_path, mgl_directory, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble):
    	
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
            
            process_datatest(prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, pdb_file_name, sdf_file_name, receptor_pdb, output_model_dir, csv_path, mgl_directory, smiles, reference_pdb, parameter, ensamble)

        except Exception as e:
            pass

    def run_parallel_molecule_processing(suppl, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for _ in tqdm(executor.map(lambda mol: process_and_save_data(mol, receptor_pdb, output_model_dir, csv_path, mgl_directory, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble), suppl),
                          total=len(suppl),
                          desc="Processing sdf molecules",
                          unit="molecule"):
                pass

    run_parallel_molecule_processing(suppl, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers)

def process_smi(smi_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble):
    # Membaca isi file SMILES
    with open(smi_file, 'r') as smi_file:
        smi_content = smi_file.read().splitlines()

    def process_and_save_data(smiles, receptor_pdb, output_model_dir, csv_path, mgl_directory, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble):
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
                process_datatest(prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, pdb_file_name, sdf_file_name, receptor_pdb, output_model_dir, csv_path, mgl_directory, smiles, reference_pdb, parameter, ensamble)

        except Exception as e:
            # Menangani exception, sesuaikan dengan kebutuhan Anda
            # print(f"Error processing SMILES: {smiles}")
            # print(f"Error details: {e}")
            pass

    def run_parallel_molecule_processing(smiles_list, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, parameter):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_and_save_data, smiles, receptor_pdb, output_model_dir, csv_path, mgl_directory, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble): smiles for smiles in smiles_list}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing smiles molecules", unit="molecule"):
                pass

    run_parallel_molecule_processing(smi_content, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, parameter)

def process_ligand_test(prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, parameter, ensamble, output_model_dir, csv_path, ligand_dir, receptor_pdb, mgl_directory, max_workers, reference_pdb):    
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
                    process_smi(smi_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble)
                    os.remove(smi_file)
                    
                for sdf_file in sdf_files:
                    process_sdf(sdf_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble)
                    os.remove(sdf_file) 
                    
        elif any(ligand_file.endswith(ext) for ext in ['.smi', 'smiles']):
            process_smi(ligand_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble)
            os.remove(ligand_file)   
            
        else:
            process_sdf(ligand_file, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, reference_pdb, parameter, ensamble)
            os.remove(ligand_file)
                 
def main():
    print_dev(developer_note, developer_contact, citation_list)
    os.chdir(current_directory)   
    model_dirs = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d)) and d.startswith('model')]
    ligand_dir = os.path.join(current_directory, 'ligand_input')
    output_dir = os.path.join(current_directory, 'output')
    config_file = os.path.join(current_directory, 'config_ladock4.txt')
    
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

    ensamble = "autodock4"
    spacing = config_variables['spacing']
    npts = config_variables['npts']
    ga_num_evals = config_variables['ga_num_evals']
    ga_pop_size = config_variables['ga_pop_size']
    ga_run = os.cpu_count()
    max_workers = os.cpu_count()     
    
    mgl_directory = config_variables['mgl_directory']
    prepare_ligand = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_ligand4.py")
    prepare_receptor = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_receptor4.py")
    prepare_gpf = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_gpf4.py")
    prepare_dpf = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "prepare_dpf4.py")
    prepare_lowest_energy = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "write_lowest_energy_ligand.py")
    prepare_summarize_result = os.path.join(mgl_directory, "MGLToolsPckgs", "AutoDockTools", "Utilities24", "summarize_results4.py")
       
    parameter = f' -p ga_num_evals={ga_num_evals} -p ga_pop_size={ga_pop_size} -p ga_run={ga_run}'

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
            process_reference(prepare_gpf, prepare_dpf, spacing, npts, max_workers, csv_path, prepare_receptor, prepare_ligand, ensamble, output_model_dir, parameter, receptor_pdb, reference_pdb)
            process_ligand_test(prepare_gpf, prepare_dpf, prepare_receptor, prepare_ligand, parameter, ensamble, output_model_dir, csv_path, ligand_dir, receptor_pdb, mgl_directory, max_workers, reference_pdb)
            sort_and_add_number(csv_path)
            print(f"Success: {model_dir_name.upper()}")
            os.chdir(current_directory)
    
        elif receptor_pdb is None or reference_pdb is None:
            print(f"Skipping {model_dir_name}: receptor or reference file not found")
            os.chdir(current_directory)
    
    # Print developer's note, contact, and citation listdir
    print_dev(developer_note, developer_contact, citation_list)
       

if __name__ == "__main__":
    current_directory =  (os.path.join(os.getcwd(), "LADOCK_ladock4")) 
    if os.path.exists(current_directory):  
        main()
    else:
        print("Your job directory (LADOCK_ladock4) is not ready. Please create it using:")
        print("ladock --create ladock4")
