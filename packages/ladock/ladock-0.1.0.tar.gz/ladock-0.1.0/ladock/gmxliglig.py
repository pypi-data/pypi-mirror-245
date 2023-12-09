#!/usr/bin/env python

import os
import subprocess
import glob
import shutil
from datetime import datetime
from main import *

def extract_ligand_id_from_mol2(mol2_file):
    lig_id = None
    with open(mol2_file, 'r') as file:
        for line in file:
            if line.startswith('HETATM'):
                # Mencari baris yang berisi ID ligand
                parts = line.split()
                if len(parts) >= 4:
                    lig_id = parts[3]
                break
    return lig_id

def process_mol2_files_in_directories(mol2_files):
    for mol2_file in mol2_files:
        lig_id = extract_ligand_id_from_mol2(mol2_file)
        print(lig_id)
        subprocess.run([f'obabel {mol2_file} -opdb -h -O {lig_id}.pdb'], shell=True)
        subprocess.run([f'acpype -i {lig_id}.pdb -c gas'], shell=True)

def create_complex_pdb(mol2_files):  
    complex_data = ""  
        
    for mol2_file in mol2_files:
        lig_id = extract_ligand_id_from_mol2(mol2_file)
        ligand_pdb = f"{lig_id}.acpype/{lig_id}_NEW.pdb"    
        with open(ligand_pdb, 'r') as ligand_file:
            ligand_data = ligand_file.read()
            complex_data += ligand_data
            
    lines = complex_data.split('\n')
    filtered_lines = [line for line in lines if not any(keyword in line for keyword in ["TITLE", "REMARK", "MODEL", "ENDMDL"])]

    with open("complex.pdb", 'w') as output_file:
        output_file.write('\n'.join(filtered_lines))
        
def create_complex_itp(mol2_files):
    atomtype_itp = ""    
    moleculetype_itp = ""
    complex_itp = ""
    
    for mol2_file in mol2_files:     
        lig_id = extract_ligand_id_from_mol2(mol2_file)
        ligand_itp = f"{lig_id}.acpype/{lig_id}_GMX.itp"         
        with open(ligand_itp, 'r') as f:        
            flag_atomtypes = False            
            flag_moleculetype = False            
            
            for line in f:                
                if '[ atomtypes ]' in line:
                    flag_atomtypes = True
                if not line.strip():
                    flag_atomtypes = False                
                if flag_atomtypes:
                        if line not in complex_itp:
                            atomtype_itp += line

                if '[ moleculetype ]' in line:                    
                    flag_moleculetype = True                
                if flag_moleculetype:
                    moleculetype_itp += line               
            complex_itp = atomtype_itp + "\n"                                 
            complex_itp += moleculetype_itp + "\n" 
    with open('complex.itp', 'w') as complex_itp_file:
        complex_itp_file.write(complex_itp)

def create_topol_top(mol2_files):
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    combined_lig_id = "_".join(extract_ligand_id_from_mol2(file) for file in mol2_files)

    with open("topol.top", 'w') as topol_file:
        topol_file.write(f"; topol.top created by ladock (v: 2023) on {current_date}\n")
        topol_file.write("\n")
        topol_file.write("; Include forcefield parameters\n")
        topol_file.write("#include \"amber99sb-ildn.ff/forcefield.itp\"\n")
        topol_file.write("\n")
        topol_file.write("; Include complex topology\n")
        topol_file.write("#include \"complex.itp\"\n")
        topol_file.write("\n")
        topol_file.write("Ligand position restraints\n")
        topol_file.write("#ifdef POSRES\n")
        for mol2_file in mol2_files:
            lig_id = extract_ligand_id_from_mol2(mol2_file)
            topol_file.write(f'#include "{lig_id}-posre.itp"\n')
        topol_file.write("#endif\n")
        topol_file.write("\n")    
        topol_file.write("; Include water topology\n")
        topol_file.write("#include \"amber99sb-ildn.ff/tip3p.itp\"\n")
        topol_file.write("\n")
        topol_file.write("#ifdef POSRES_WATER\n")
        topol_file.write("; Position restraint for each water oxygen\n")
        topol_file.write("[ position_restraints ]\n")
        topol_file.write("   1    1       1000       1000       1000\n")
        topol_file.write("#endif\n")
        topol_file.write("\n")
        topol_file.write("; Include topology for ions\n")
        topol_file.write("#include \"amber99sb-ildn.ff/ions.itp\"\n")
        topol_file.write("\n")
        topol_file.write("[ system ]\n")
        topol_file.write(f"{combined_lig_id}\n")
        topol_file.write("\n")
        topol_file.write("[ molecules ]\n")
        for file in mol2_files:
            lig_id = extract_ligand_id_from_mol2(file)
            topol_file.write(f"{lig_id}                  1\n")
   
def generate_box_pdb(input_pdb, box_pdb, box_type, distance):
    try:
        editconf_cmd = f"gmx editconf -f {input_pdb} -o {box_pdb} -bt {box_type} -d {distance} -c"
        subprocess.run(editconf_cmd, shell=True)      
    except subprocess.CalledProcessError:    
        pass 

def solvate_system(box_pdb, spc216_gro, topol_top, solv_gro):
    try:
        solvate_cmd = f"gmx solvate -cp {box_pdb} -cs {spc216_gro} -p {topol_top} -o {solv_gro}"
        subprocess.run(solvate_cmd, shell=True)      
    except subprocess.CalledProcessError:
        pass

def ionization(solv_gro, topol_top, ions_gro):
    try:
        # Generate TPR file
        grompp_cmd = f"gmx grompp -f ions.mdp -c solv_gro -p topol_top -o ions.tpr maxwarn 1"
        subprocess.run(grompp_cmd, shell=True)            

        # Run genion for ionization
        genion_cmd = f"gmx genion -s ions.tpr -o {ions_gro} -p {topol_top} -pname NA -nname CL -neutral"
        subprocess.run(genion_cmd, shell=True)    
    except subprocess.CalledProcessError:
        pass
  
def minimization(ions_gro, topol_top):
    try:
        # Generate TPR file for minimization
        grompp_cmd = f"gmx grompp -f em.mdp -c {ions_gro} -p {topol_top} -o em.tpr -maxwarn 1"
        subprocess.run(grompp_cmd, shell=True)
        
        # Run energy minimization using mdrun
        mdrun_cmd = f"gmx mdrun -v -deffnm em"
        subprocess.run(mdrun_cmd, shell=True)
        
        # Calculate potential energy
        energy_cmd = f"echo -e '10\n0' | gmx energy -f em.edr -o potential.xvg"
        subprocess.run(energy_cmd, shell=True)
    except subprocess.CalledProcessError:
        pass
 
def make_index_system(em_gro, index_ndx):
    try:
        # Create index file for the system
        make_ndx_cmd = f"gmx make_ndx -f {em_gro} -o {index_ndx}"
        subprocess.run(make_ndx_cmd, shell=True)
    except subprocess.CalledProcessError:
        pass

def process_ligand_restraint(mol2_files):
    for mol2_file in mol2_files:
        lig_id = extract_ligand_id_from_mol2(mol2_file)
        ligand_new_pdbs = glob.glob(f"{lig_id}.acpype/{lig_id}_NEW.pdb")
        
        for ligand_new_pdb in ligand_new_pdbs:
            try:
                # Perintah untuk membuat indeks
                make_ndx_command = f'echo "2 & ! a H*\nq\n" | gmx make_ndx -f {ligand_new_pdb} -o {lig_id}-index.ndx'
                subprocess.run(make_ndx_command, shell=True)
                
                # Perintah untuk menjalankan genrestr
                genrestr_command = f'echo "3\n" | gmx genrestr -f {ligand_new_pdb} -n {lig_id}-index.ndx -o {lig_id}-posre.itp -fc 1000 1000 1000'
                subprocess.run(genrestr_command, shell=True)
            except subprocess.CalledProcessError as e:
                pass

def copy_mdp_files(current_directory, subdir):
    mdp_files = glob.glob(os.path.join(current_directory, "*.mdp"))    
    try:
        for mdp_file in mdp_files:
            mdp_filename = os.path.basename(mdp_file)
            destination_path = os.path.join(".", mdp_filename)
            shutil.copyfile(mdp_file, mdp_filename)
    except Exception as e:
        pass
            
def replace_text_in_files(mol2_files):
    mdp_files = glob.glob(os.path.join(".", "*.mdp"))
    ligand_ids = [extract_ligand_id_from_mol2(file) for file in mol2_files]    
   
    if None in ligand_ids:
        # Handle cases where ligand_id extraction fails
        print("Error: Some ligand IDs could not be extracted.")
        return
    
    combined_lig_id = "_".join(ligand_ids)
    
    for mdp_file in mdp_files:
        with open(mdp_file, 'r') as file:
            file_data = file.read()
            file_data = file_data.replace("Protein_UNK", combined_lig_id)
            
            # Check if 'ions' is present in the file_data
            if "ions" in file_data:
                file_data = file_data.replace("Water_and_ions", "Water")

        with open(mdp_file, 'w') as file:
            file.write(file_data)

def run_nvt_simulation():
    # Jalankan grompp untuk NVT
    grompp_cmd = f"gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 5"
    subprocess.run(grompp_cmd, shell=True, check=True)

    # Jalankan mdrun untuk NVT
    mdrun_cmd = f"gmx mdrun -v -s nvt.tpr -deffnm nvt"
    subprocess.run(mdrun_cmd, shell=True, check=True)

def run_npt_simulation():
    # Jalankan grompp untuk NPT
    grompp_cmd = f"gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -n index.ndx -o npt.tpr -maxwarn 5"
    subprocess.run(grompp_cmd, shell=True, check=True)

    # Jalankan mdrun untuk NPT
    mdrun_cmd = f"gmx mdrun -v -s npt.tpr -deffnm npt"
    subprocess.run(mdrun_cmd, shell=True, check=True)

def run_production_simulation():
    # Jalankan grompp untuk produksi
    grompp_cmd = f"gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md.tpr -maxwarn 5"
    subprocess.run(grompp_cmd, shell=True, check=True)

    # Jalankan mdrun untuk produksi
    mdrun_cmd = f"gmx mdrun -v -s md.tpr -deffnm md"
    subprocess.run(mdrun_cmd, shell=True, check=True)

def print_dev(developer_note, developer_contact, citation_list):
    print("")
    print(developer_note)
    print("")
    print(developer_contact)
    print("")
    print(citation_list)
    print("")

def main():
    print_dev(developer_note, developer_contact, citation_list)
    # Membaca isi file 'config_tmp.txt'
    with open('config_gmxliglig.txt', 'r') as config_file:
        config_lines = config_file.readlines()
    
    # Membuat kamus (dictionary) untuk menyimpan variabel-variabel
    config_variables = {}

    # Memproses setiap baris dalam file 'config.txt'
    for line in config_lines:
            # Mengabaikan baris yang dimulai dengan '#' (komentar)
            if not line.strip().startswith('#'):
                # Memisahkan nama variabel dan nilai variabel
                try:
                    name, value = line.strip().split('=')
                    # Membersihkan spasi dan karakter lainnya
                    name = name.strip()
                    value = value.strip()
                    # Menambahkan variabel ke dalam kamus
                    config_variables[name] = value
                except ValueError:
                    pass

    box_type = config_variables['box_type']
    distance = config_variables['distance']
    spc216_gro = config_variables['coordinate_file']
    current_directory = os.getcwd()  
    input_pdb = "complex.pdb"  
    box_pdb = "box.pdb"    
    topol_top = "topol.top"    
    solv_gro = "solv.gro" 
    ions_gro = "ions.gro"
    em_gro = "em.gro"
    index_ndx = "index.ndx"
    
    for subdir in os.listdir(current_directory):
        if os.path.isdir(subdir):
            os.chdir(subdir)         
            temp_files = glob.glob('#*')           
            for temp_file in temp_files:
                os.remove(temp_file)                        
            mol2_files = glob.glob('lig_*.pdb')
            copy_mdp_files(current_directory, subdir)       
            replace_text_in_files(mol2_files)
            process_mol2_files_in_directories(mol2_files)             
            create_complex_pdb(mol2_files)     
            create_complex_itp(mol2_files)
            create_topol_top(mol2_files)
            generate_box_pdb(input_pdb, box_pdb, box_type, distance)
            solvate_system(box_pdb, spc216_gro, topol_top, solv_gro)
            ionization(solv_gro, topol_top, ions_gro)
            minimization(ions_gro, topol_top)
            process_ligand_restraint(mol2_files)
            make_index_system(em_gro, index_ndx)            
            os.chdir('..')
            
    for subdir in os.listdir(current_directory):
        if os.path.isdir(subdir):
            os.chdir(subdir)         
            run_nvt_simulation()
            run_npt_simulation()
            run_production_simulation()            
            os.chdir('..')
            
    print_dev(developer_note, developer_contact, citation_list)
    
if __name__ == "__main__":
    current_directory =  (os.path.join(os.getcwd(), "LADOCK_gmxliglig"))      
    
    if os.path.exists(current_directory):
        os.chdir(current_directory)
        main() 
    else:
        print("Your job directory (LADOCK_gmxliglig) is not ready. Please create it using:")
        print("ladock --create gmxliglig")
