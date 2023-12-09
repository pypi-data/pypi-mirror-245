#!/usr/bin/env python3

import os
import sys
import argparse
import glob
import shutil
import subprocess

source_directory = os.path.dirname(os.path.abspath(__file__))
config_directory = os.path.join(source_directory, "config")
share_directory = os.path.join(source_directory, "share")
mdp_directory = os.path.join(source_directory, "share", "mdp")
preparedata_dir = os.path.join(source_directory, "PrepareData")
tensor_dir = os.path.join(source_directory, "tensor")
knn_dir = os.path.join(source_directory, "knn")
rf_dir = os.path.join(source_directory, "rf")
vina = os.path.join(share_directory, "vina_1.2.5_linux_x86_64")
vina_split = os.path.join(share_directory, "vina_split_1.2.5_linux_x86_64")

dn = os.path.join(source_directory, "developerNote.txt")
with open(dn, 'r') as file:
    content = file.read()

# Pisahkan isi file menjadi blok-blok yang sesuai dengan variabel-variabel
blocks = content.split('\n\n')
# Inisialisasi variabel
developer_note = ""
developer_contact = ""
citation_list = ""

# Loop melalui blok-blok dan mengisi variabel yang sesuai
for block in blocks:
    if block.startswith("developer_note ="):
        developer_note = block[block.find("=") + 1:].strip()
    elif block.startswith("developer_contact ="):
        developer_contact = block[block.find("=") + 1:].strip()
    elif block.startswith("citation_list ="):
        citation_list = block[block.find("=") + 1:].strip()

def create_lavina():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_lavina'):
        os.mkdir('LADOCK_lavina')
    os.chdir('LADOCK_lavina')

    if not os.path.exists('ligand_input'):
        os.mkdir('ligand_input')
   
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'model_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

    # Mengambil isi 'config_content' dari file 'lavinaConfig.py'
    from ladock.config.lavinaConfig import config_content
    with open('config_lavina.txt', 'w') as config_file:
        config_file.write(config_content)

    # Mengambil isi 'ligand_link_default' dari file 'lavinaConfig.py'
    from ladock.config.lavinaConfig import ligand_link_default
    ligand_input_dir = os.path.join('ligand_input', 'ligand_link.txt')   
    with open(ligand_input_dir, 'w') as ligand_link_file:
        ligand_link_file.write(ligand_link_default) 
        
def create_lavinadl():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_lavinadl'):
        os.mkdir('LADOCK_lavinadl')
    os.chdir('LADOCK_lavinadl')

    if not os.path.exists('ligand_input'):
        os.mkdir('ligand_input')
   
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'model_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

    # Mengambil isi 'config_content' dari file 'lavinaConfig.py'
    from ladock.config.lavinadlConfig import config_content
    with open('config_lavinadl.txt', 'w') as config_file:
        config_file.write(config_content)

    # Mengambil isi 'ligand_link_default' dari file 'lavinaConfig.py'
    from ladock.config.lavinadlConfig import ligand_link_default
    ligand_input_dir = os.path.join('ligand_input', 'ligand_link.txt')   
    with open(ligand_input_dir, 'w') as ligand_link_file:
        ligand_link_file.write(ligand_link_default) 
 
def create_lavinagpu():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_lavinagpu'):
        os.mkdir('LADOCK_lavinagpu')
    os.chdir('LADOCK_lavinagpu')

    if not os.path.exists('ligand_input'):
        os.mkdir('ligand_input')
   
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'model_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

    # Mengambil isi 'config_content' dari file 'lavinagpuConfig.py'
    from ladock.config.lavinagpuConfig import config_content
    with open('config_lavinagpu.txt', 'w') as config_file:
        config_file.write(config_content)

    # Mengambil isi 'ligand_link_default' dari file 'lavinaConfig.py'
    from ladock.config.lavinagpuConfig import ligand_link_default
    ligand_input_dir = os.path.join('ligand_input', 'ligand_link.txt')   
    with open(ligand_input_dir, 'w') as ligand_link_file:
        ligand_link_file.write(ligand_link_default) 
        
def create_la2vina():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_la2vina'):
        os.mkdir('LADOCK_la2vina')
    os.chdir('LADOCK_la2vina')

    if not os.path.exists('ligand_input'):
        os.mkdir('ligand_input')

    if not os.path.exists('main_ligand'):
        os.mkdir('main_ligand')
    
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'model_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

    # Mengambil isi 'config_content' dari file 'la2vinaConfig.py'
    from ladock.config.la2vinaConfig import config_content
    with open('config_la2vina.txt', 'w') as config_file:
        config_file.write(config_content)

    # Mengambil isi 'ligand_link_default' dari file 'lavinaConfig.py'
    from ladock.config.lavinaConfig import ligand_link_default    
    ligand_input_dir = os.path.join('ligand_input', 'ligand_link.txt')   
    with open(ligand_input_dir, 'w') as ligand_link_file:
        ligand_link_file.write(ligand_link_default)
       
def create_ladock4():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_ladock4'):
        os.mkdir('LADOCK_ladock4')
    os.chdir('LADOCK_ladock4')

    if not os.path.exists('ligand_input'):
        os.mkdir('ligand_input')
    
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'model_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

    # Mengambil isi 'config_content' dari file 'ladock4Config.py'
    from ladock.config.ladock4Config import config_content
    with open('config_ladock4.txt', 'w') as config_file:
        config_file.write(config_content)

    # Mengambil isi 'ligand_link_default' dari file 'ladock4Config.py'
    from ladock.config.ladock4Config import ligand_link_default
    ligand_input_dir = os.path.join('ligand_input', 'ligand_link.txt')   
    
    with open(ligand_input_dir, 'w') as ligand_link_file:
        ligand_link_file.write(ligand_link_default)
        
def create_ladockgpu():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_ladockgpu'):
        os.mkdir('LADOCK_ladockgpu')
    os.chdir('LADOCK_ladockgpu')

    if not os.path.exists('ligand_input'):
        os.mkdir('ligand_input')
    
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'model_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)

    # Mengambil isi 'config_content' dari file 'ladock4Config.py'
    from ladock.config.ladockgpuConfig import config_content
    with open('config_ladockgpu.txt', 'w') as config_file:
        config_file.write(config_content)

    # Mengambil isi 'ligand_link_default' dari file 'ladockGPUConfig.py'
    from ladock.config.ladockgpuConfig import ligand_link_default
    ligand_input_dir = os.path.join('ligand_input', 'ligand_link.txt')   
    
    with open(ligand_input_dir, 'w') as ligand_link_file:
        ligand_link_file.write(ligand_link_default)      

def create_gmxprolig():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_gmxprolig'):
        os.mkdir('LADOCK_gmxprolig')
    os.chdir('LADOCK_gmxprolig')
   
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'complex_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
    
    current_directory = os.getcwd()
    destination_dir = os.getcwd()
    for filename in os.listdir(mdp_directory):
        if filename.endswith(".mdp"):
            source_file = os.path.join(mdp_directory, filename)
            destination_file = os.path.join(destination_dir, filename)
            shutil.copy(source_file, destination_file)

    # Mengambil isi 'config_content' dari file 'lagmxConfig.py'
    from ladock.config.gmxproligConfig import config_content
    with open('config_gmxprolig.txt', 'w') as config_file:
        config_file.write(config_content)
        
def create_gmxliglig():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('LADOCK_gmxliglig'):
        os.mkdir('LADOCK_gmxliglig')
    os.chdir('LADOCK_gmxliglig')
    
    for i in range(1, 4):  # Membuat direktori model_01, model_02, model_03, model_04
        model_dir = f'complex_{i:02d}'
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
    
    current_directory = os.getcwd()
    destination_dir = os.getcwd()
    for filename in os.listdir(mdp_directory):
        if filename.endswith(".mdp"):
            source_file = os.path.join(mdp_directory, filename)
            shutil.copy(source_file, current_directory)

    # Mengambil isi 'config_content' dari file 'ligligConfig.py'
    from ladock.config.gmxligligConfig import config_content
    with open('config_gmxliglig.txt', 'w') as config_file:
        config_file.write(config_content)

def create_getdata_s3():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('getdata_input'):     
        os.mkdir('getdata_input')
    if not os.path.exists('getdata_output'):     
        os.mkdir('getdata_output')
    if not os.path.exists('preparedataConfig'):
        shutil.copy(os.path.join(preparedata_dir, 'preparedataConfig'), '.')
        
def create_getdata_s1():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('getdata1Config'):
        shutil.copy(os.path.join(config_directory, 'chembl_query.txt'), '.')

def create_getdata_s2():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('getdata1Config'):
        shutil.copy(os.path.join(config_directory, 'targets_exp.csv'), '.')

def create_getdata_s3():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('getdata_input'):     
        os.mkdir('getdata_input')
    if not os.path.exists('getdata_output'):     
        os.mkdir('getdata_output')
    if not os.path.exists('preparedataConfig'):
        shutil.copy(os.path.join(preparedata_dir, 'preparedataConfig'), '.')

def create_tensor():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('tensor_input'):     
        os.mkdir('tensor_input')
    if not os.path.exists('tensor_output'):     
        os.mkdir('tensor_output')
    if not os.path.exists('tensorConfig'):
        shutil.copy(os.path.join(tensor_dir, 'tensorConfig'), '.')

def create_knn():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('knn_input'):     
        os.mkdir('knn_input')
    if not os.path.exists('knn_output'):     
        os.mkdir('knn_output')
    if not os.path.exists('knnConfig'):
        shutil.copy(os.path.join(knn_dir, 'knnConfig'), '.')

def create_rf():
    # Membuat struktur direktori dan file konfigurasi di dalamnya
    if not os.path.exists('rf_input'):     
        os.mkdir('rf_input')
    if not os.path.exists('rf_output'):     
        os.mkdir('rf_output')
    if not os.path.exists('rfConfig'):
        shutil.copy(os.path.join(rf_dir, 'rfConfig'), '.')

def create_input(simulation_type):
    if simulation_type == 'lavina':
        create_lavina()
        print("LADOCK_lavina, subdirectories, 'config_lavina.txt', and 'ligand_link.txt' have been successfully created in the 'LADOCK_lavina' directory. Please edit them according to your needs.")
    
    if simulation_type == 'lavinagpu':   
        create_lavinagpu()
        print("LADOCK_lavinagpu, subdirectories, 'config_lavina.txt', and 'ligand_link.txt' have been successfully created in the 'LADOCK_lavinagpu' directory. Please edit them according to your needs.")
        
    elif simulation_type == 'lavinadl':   
        create_lavinadl()
        print("LADOCK_lavinadl, subdirectories, 'config_lavinadl.txt', and 'ligand_link.txt' have been successfully created in the 'LADOCK_lavinagpu' directory. Please edit them according to your needs.")

    elif simulation_type == 'la2vina':
        create_la2vina()
        print("LADOCK_la2vina, subdirectories, and 'config_la2vina.txt' have been successfully created in the 'LADOCK_la2vina' directory. Please edit them according to your needs.")

    elif simulation_type == 'ladock4':
        create_ladock4()
        print("LADOCK_ladock4, subdirectories, 'config_ladock4.txt', and 'ligand_link.txt' have been successfully created in the 'LADOCK_ladock4' directory. Please edit them according to your needs.")

    elif simulation_type == 'ladockgpu':
        create_ladockgpu()
        print("LADOCK_ladockgpu, subdirectories, 'config_ladockgpu.txt', and 'ligand_link.txt' have been successfully created in the 'LADOCK_ladockgpu' directory. Please edit them according to your needs.")

    elif simulation_type == 'gmxprolig':
        create_gmxprolig()
        print("LADOCK_gmxprolig and subdirectory created successfully.")
       
    elif simulation_type == 'gmxliglig':
        create_gmxliglig()
        print("LADOCK_gmxliglig and subdirectory created successfully.")
        
    elif simulation_type == 'getdata_s3':
        create_preparedata()
        print("conflig file, and input, output directories for prepare-data created successfully.")

    elif simulation_type == 'getdata_s1':
        create_getdata_s1()
        print("chembl_query.txt file for getdata-s1 created successfully.")
        
    elif simulation_type == 'getdata_s2':
        create_getdata_s2()
        print("target_exp.csv file for getdata-s2 created successfully.")
        
    elif simulation_type == 'tensor':
        create_tensor()
        print("conflig file and input, output directories for tensorflow modeling created successfully.")

    elif simulation_type == 'knn':
        create_knn()
        print("conflig file and input, output directories for K-Nearest Neighbors modeling created successfully.")

    elif simulation_type == 'rf':
        create_rf()
        print("conflig file and input, output directories for Random Forest modeling created successfully.")

def run_simulation(simulation_type):
    
    if simulation_type == 'lavina':        
        from ladock.config import lavinaConfig
        path = os.path.join(source_directory, 'lavina.py')
        subprocess.run(['python3', path])
        
    elif simulation_type == 'lavinagpu':        
        from ladock.config import lavinagpuConfig
        path = os.path.join(source_directory, 'lavinagpu.py')
        subprocess.run(['python3', path])
   
    elif simulation_type == 'lavinadl':        
        from ladock.config import lavinadlConfig
        path = os.path.join(source_directory, 'lavinaDL.py')
        subprocess.run(['python3', path])

    elif simulation_type == 'la2vina':
        from ladock.config import la2vinaConfig
        path = os.path.join(source_directory, 'la2vina.py')
        subprocess.run(['python3', path])

    elif simulation_type == 'ladock4':
        from ladock.config import ladock4Config
        path = os.path.join(source_directory, 'ladock4.py')
        subprocess.run(['python3', path])

    elif simulation_type == 'ladockgpu':
        from ladock.config import ladockgpuConfig
        path = os.path.join(source_directory, 'ladockgpu.py')
        subprocess.run(['python3', path])

    elif simulation_type == 'gmxprolig':
        from ladock.config import gmxproligConfig
        path = os.path.join(source_directory, 'gmxprolig.py')
        subprocess.run(['python3', path])        
       
    elif simulation_type == 'gmxliglig':
        from ladock.config import gmxligligConfig
        path = os.path.join(source_directory, 'gmxliglig.py')
        subprocess.run(['python3', path])
        
    elif simulation_type == 'test':
        from ladock.config import testConfig
        path = os.path.join(source_directory, 'test.py')
        subprocess.run(['python3', path])
        
    elif simulation_type == 'getdata_s1':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, 'getData_S1.py')
        subprocess.run(['python3', path])
   
    elif simulation_type == 'getdata_s2':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, 'getData_S2.py')
        subprocess.run(['python3', path])
        
    elif simulation_type == 'getdata_s3':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, 'PrepareData', 'main.py')
        subprocess.run(['python3', path])
        
    elif simulation_type == 'tensor':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, 'tensor', 'tensor.py')
        subprocess.run(['python3', path])
        
    elif simulation_type == 'knn':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, 'knn', 'knn.py')
        subprocess.run(['python3', path])

    elif simulation_type == 'rf':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, 'rf', 'rfs.py')
        subprocess.run(['python3', path])

def main():
    
    parser = argparse.ArgumentParser(description='LADOCK is an innovative and free tool designed for conducting simultaneous simulations in computer-aided drug discovery, encompassing molecular docking and molecular dynamics. In molecular docking, LADOCK excels in handling single or double ligands. It supports ligands from various online sources. In molecular dynamics, LADOCK efficiently manages protein-ligand interactions and even ligand-ligand interactions, accommodating scenarios with one or multiple proteins and ligands.')
    parser.add_argument('--version', action='version', version='ladock 0.1.0')
    parser.add_argument('--create', choices=['lavina', 'lavinagpu', 'lavinadl', 'la2vina', 'ladock4', 'ladockgpu', 'gmxprolig', 'getdata_s1', 'getdata_s2', 'getdata_s3', 'gmxliglig', 'tensor', 'knn', 'rf'], help='Create necessary input')
    parser.add_argument('--run', choices=['lavina', 'lavinagpu', 'lavinadl', 'la2vina', 'ladock4', 'ladockgpu', 'gmxprolig', 'gmxliglig', 'getdata_s1', 'getdata_s2', 'getdata_s3', 'tensor', 'knn', 'rf'], help='Execute the specific simulation: lavina (AutoDock Vina), lavinagpu (AutoDock Vina with GPU), lavinadl (Combining AutoDock Vina and Deep Learning), la2vina (MLSD with Autodock Vina), ladock4 (AutoDock4), ladockgpu (AutoDock-GPU), gmxprolig (gromacs for 1 protein with 1 or multiple ligands), gmxliglig (gromacs multiple ligands)' )
    args = parser.parse_args()

    if args.create:
        create_input(args.create)

    elif args.run:
        print("RUNNING")
        run_simulation(args.run)
    
    else:
        print("Invalid option. Please use one of the following:")
        print("'--create lavina' to create input for AutoDock Vina simulation.")
        print("'--create lavinagpu' to create input for AutoDock Vina GPU simulation.")
        print("'--create lavinadl' to create input for AutoDock Vina - Deep Learning.")
        print("'--create la2vina' to create input for AutoDock Vina simulation using multiple ligand simultaneously molecular-docking technique).")
        print("'--create ladock4' to create input for AutoDock4 simulation.")
        print("'--create ladockgpu' to create input for AutoDock4-GPU simulation.")
        print("'--create gmxprolig' to create input for single or multiple ligand simultaneously molecular dynamics simulation with GROMACS.")
        print("'--create gmxliglig' to create input for single/multiple ligand and single/multiple (chain) protein simultaneously molecular dynamics simulation with GROMACS")
        print("'--create getdata_s1' to create config for get data step 1 from ChemBl: based on queries.")
        print("'--create getdata_s2' to create config for get data step 2 from ChemBl: based on target ChemBl IDs.")
        print("'--create getdata_s3' to create config for get data step 3 from ChemBl: based on molecule ChemBl IDs.")
        print("'--create tensor' to create config for generate deep learning model using tensorflow.")
        print("'--create knn to create config for generate deep learning model using K-Nearest Neighbors.")
        print("'--create rf' to create config for generate deep learning model using Random Forest.")
        print("'--run lavina' for docking simulation with AutoDock Vina.")
        print("'--run la2vina' for docking simulation with AutoDock Vina using MLSD (multiple ligand simulation docking technique).")
        print("'--run ladock4' for docking simulation with AutoDock4.")
        print("'--run ladockgpu' for docking simulation with AutoDock-GPU.")
        print("'--run gmxprolig' for single or multiple ligand simultaneously molecular dynamics simulation with GROMACS.")
        print("'--run gmxliglig' for single/multiple ligand and single/multiple (chain) protein simultaneously molecular dynamics simulation with GROMACS")
        print("'--run getdata_s1' for get data step 1 from ChemBl: based on queries.")
        print("'--run getdata_s2' for get data step 2 from ChemBl: based on target ChamBel IDs.")
        print("'--run getdata_s3' for get data step 3 from ChemBl: based on molecule ChemBl IDs.")
        print("'--run tensor' for generate deep learning model using tensorflow.")
        print("'--run rf' for generate deep learning model using Random Forest.")
        print("'--run knn' for generate deep learning model using K-Nearest Neighbors.")
        print("'--version' to show the LADOCK's version number.")
        print("'--help' or '-h' for help.")
        print("\nNote: Ensure that the following dependency packages are installed on your system:")
        print("* autodock4")
        print("* autodock-gpu")
        print("* autodock vina")
        print("* vina-gpu")
        print("* mgltools")
        print("* gromacs")
        print("* acpype")
        print("* rdkit")
        print("* tensorflow")
    
if __name__ == "__main__":
    
    main()
