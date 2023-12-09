import os
import requests
import gzip
from tqdm import tqdm
from multiprocessing import Pool
from rdkit import Chem
from rdkit.Chem import AllChem
from os.path import basename, splitext
from mgl import convert_to_pdbqt, docking_vina
from mol_prep import mol_opt_sdf
from dir_def import current_dir, model_dirs, ligand_dir, output_dir

def download_file(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for data in tqdm(response.iter_content(chunk_size=1024), desc='Downloading'):
            file.write(data)

def extract_gz(file_path):
    with gzip.open(file_path, 'rb') as f_in, open(file_path[:-3], 'wb') as f_out:
        f_out.write(f_in.read())

def process_sdf(molecule_file):
    with open(molecule_file, 'r') as sdf_file:
        sdf_content = sdf_file.read()
    molecules = sdf_content.split("$$$$")

    for mol in molecules:
        if not mol.strip():
            continue  
        Chem.MolToPDBFile(mol, pdb_ligand)    
        process_datatest(receptor_pdb, reference_pdb, pdb_ligand, output_model_dir, config_file)

def process_ligand_test(model_dir, x_center, y_center, z_center, size_x, size_y, size_z, vina_score, cpu):    
    for ligand_file in os.listdir(ligand_dir):
        if ligand_file.endswith('.txt'):
            file_path = os.path.join(ligand_dir, ligand_file)
            with open(file_path, 'r') as file:
                ligand_links = [line.strip() for line in file.readlines()]

            for ligand_link in ligand_links:
                ligand_file_base = basename(ligand_link)
                ligand_name = splitext(ligand_file_base)[0]
                download_file(ligand_link, ligand_file_base)
                
                if ligand_file_base.endswith('.gz'):
                    extract_gz(ligand_file_base)
                    os.remove(ligand_file_base+'.gz')
                
                smi_files = [f for f in os.listdir(.) if f.endswith(".smi")]
                sdf_files = [f for f in os.listdir(.) if f.endswith(".sdf")]
                
                for smiles in smi_files :
                    process_smi(smi_file)
                    os.remove(smi_file)
                
                for sdf in sdf_files :
                    process_smi(sdf)
                    os.remove(sdf) 
                
def main():
    os.chdir(current_dir)    
    max_works = os.cpu_count() - 2 

    for model_dir in model_dirs:
        os.chdir(model_dir)
        print(f"  Docking and save energy of ligand reference") 
        x_center, y_center, z_center, size_x, size_y, size_z, cpu = process_reference(receptor_pdb, reference_pdb, output_model_dir, config_file)
        process_ligand_test(model_dir, x_center, y_center, z_center, size_x, size_y, size_z, cpu)
        os.chdir(current_dir)

if __name__ == "__main__":
    main()