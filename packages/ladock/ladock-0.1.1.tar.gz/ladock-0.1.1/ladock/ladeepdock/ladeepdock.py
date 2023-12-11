import os
import random
import sys  
import shutil
import pandas as pd
import threading
from ladock.main import *
from ladock.lavina import process_reference, process_smi, process_sdf
from ladock.tensor.tf import generate_model
from ladock.ladeepdock.testing_model import testing_model
from ladock.ladeepdock.prepare_data import prepareData, process_ligand_test
from ladock.utility import print_dev, delete_files_except_pdb, download_file_with_retry, sort_and_add_number
from os.path import basename, splitext
from ladock.ladeepdock.config import lismode, act_log, activity, columns_to_remove, act_log, act_plot, transformX, transformY, scalerX, scalerY, ephocs, batch_size, dense_units, optimizer, all_features, lismode, mode_2d, mode_3d, mode_fp, input_column
import time


def summaries_energy(output_model_dir, pdbqt_output, receptor_pdb):
    vina_output_file = os.path.join(output_model_dir, pdbqt_output)

    with open(vina_output_file, 'r') as vina_output:
        lines = vina_output.readlines()

    energy_list = []
    model_list = []

    for line in lines:
        if "REMARK VINA RESULT:" in line:
            energy = float(line.split()[3])
            energy_list.append(energy)
        elif "MODEL" in line:
            model = int(float(line.split()[1]))
            model_list.append(model)

    if energy_list:
        print("Summary Data:")
        for model, energy in zip(model_list, energy_list):
            print(f'Model {model}: {energy} kcal/mol')
                       
    else:
        print(f"No docking_result found in the output of {os.path.basename(pdbqt_output)}")


def ask_to_continue():
    user_input = None
    def get_user_input():
        nonlocal user_input
        user_input = input("\nContinue the process? (Yes/No): ").lower()
    input_thread = threading.Thread(target=get_user_input)
    input_thread.start()
    input_thread.join(timeout=10)
    if input_thread.is_alive():
        print("\nNo response received. The process continues...")
    else:
        if user_input == "no":
            print("\nThe process is canceled.")
            sys.exit()
        elif user_input == "yes" or user_input == "":
            print("\nThe process continues...")
        else:
            print("\nIncorrect input.")

def run_simulation():
    total_time_start = time.time()

    print("Simulation started...")

    # Stage 1
    start_time = time.time()
    reference_ligand_docking()
    end_time = time.time()
    print(f"Stage 1: Reference Ligand Docking - Time: {end_time - start_time} seconds")

    # Stage 2
    start_time = time.time()
    training_set_docking()
    end_time = time.time()
    print(f"Stage 2: Training Set Docking - Time: {end_time - start_time} seconds")

    # Stage 3
    start_time = time.time()
    training_set_descriptors_calculation()
    end_time = time.time()
    print(f"Stage 3: Training Set Descriptors Calculation - Time: {end_time - start_time} seconds")

    # Stage 4
    start_time = time.time()
    generate_deep_model()
    end_time = time.time()
    print(f"Stage 4: Generate Deep Model - Time: {end_time - start_time} seconds")

    # Stage 5
    start_time = time.time()
    test_set_descriptors_calculation()
    end_time = time.time()
    print(f"Stage 5: Test Set Descriptors Calculation - Time: {end_time - start_time} seconds")

    # Stage 6
    start_time = time.time()
    test_set_deep_score_calculation()
    end_time = time.time()
    print(f"Stage 6: Test Set Deep Score Calculation - Time: {end_time - start_time} seconds")

    total_time_end = time.time()
    total_time = total_time_end - total_time_start
    print(f"Total simulation time: {total_time} seconds")

def main():
    os.chdir(current_dir)
    model_dirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d)) and d.startswith('model')]
    ligand_dir = os.path.join(current_dir, 'ligand_input')
    output_dir = os.path.join(current_dir, 'output')
    config_file = os.path.join(current_dir, 'ladeepdockConfig')

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

    mgl_directory = config_variables.get('mgl_directory', '')

    ensemble = 'vina'
    num_modes = int(config_variables.get('num_modes', 0))  # Convert to integer
    exhaustiveness = int(config_variables.get('exhaustiveness', 0))  # Convert to integer
    num_iterations = 1000
    cpu = os.cpu_count()

    size_x = float(config_variables.get('size_x', 0.0))
    size_y = float(config_variables.get('size_y', 0.0))
    size_z = float(config_variables.get('size_z', 0.0))

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
        os.chdir(model_dir)  # Make sure to return to the initial directory before changing directories
        model_dir_name = os.path.basename(model_dir)
        

        # Find files with prefixes "rec" for receptor and "lig" for reference
        receptor_pdb = next((f for f in os.listdir('.') if f.startswith("rec") and f.endswith(".pdb")), None)
        reference_pdb = next((f for f in os.listdir('.') if f.startswith("lig") and f.endswith(".pdb")), None)

        if receptor_pdb and reference_pdb:
            delete_files_except_pdb(receptor_pdb, reference_pdb)

            # Create an output directory for each model
            output_model_dir = os.path.join(output_dir, model_dir_name)
            os.makedirs(output_model_dir, exist_ok=True)

            # Create energy_summary.csv file
            csv_path = os.path.join(output_model_dir, f"{model_dir_name}.csv")
            with open(csv_path, 'w') as csv_file:
                csv_file.write("ligand_id, smiles, docking_score\n")

            print(f"\nProcessing {model_dir_name} - Docking and save energy of ligand reference")
            time.sleep(2)
            pdbqt_output, x_center, y_center, z_center, size_x, size_y, size_z = process_reference(receptor_pdb,
                                                                                                   reference_pdb,
                                                                                                   output_model_dir, csv_path,
                                                                                                   size_x, size_y, size_z,
                                                                                                   num_modes,
                                                                                                   exhaustiveness, cpu,
                                                                                                   mgl_directory,
                                                                                                   max_workers)

            summaries_energy(output_model_dir, pdbqt_output, receptor_pdb)
            
            # Docking with vina
            print("\nThe next is trainingset docking with vina")
            ask_to_continue() 
            
            valid_extensions = (".txt")
            valid_lines = []
            total_links = 0

            ligand_link_files = [f for f in os.listdir(ligand_dir) if any(f.endswith(ext) for ext in valid_extensions)]

            # Iterate through ligand_link files once
            for ligand_link_file in ligand_link_files: 
                ligand_link_path = os.path.join (ligand_dir, ligand_link_file)
                with open(ligand_link_path, 'r') as f:   
                    lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
                    for line in lines:
                        valid_lines.append(line)
                    total_links += len(lines)
                               
            if len(valid_lines) < 5:
                 num_lines_to_take = 1  # Take one line if valid_lines is less than 5
            elif len(valid_lines) < 100:
                 num_lines_to_take = int(0.1 * len(valid_lines))  # Take 10% if valid_lines is less than 100
            elif len(valid_lines) < 1000:
                num_lines_to_take = int(0.01 * len(valid_lines))  # Take 1% if valid_lines is less than 1000
            else:
                num_lines_to_take = int(0.002 * len(valid_lines))  # Take 0.1% if valid_lines is 1000 or more
                
            # Shuffle and take the specified number of lines randomly
            random.shuffle(valid_lines)
            vina_lines = valid_lines[:num_lines_to_take]
            #vina_lines = ['http://files.docking.org/2D/AA/AABD.smi']
            
            valid_lines_set = set(valid_lines)
            vina_lines_set = set(vina_lines)
            dl_lines_set = valid_lines_set - vina_lines_set
            dl_lines = list(dl_lines_set)
            links_for_vina_docking = len(vina_lines)
            links_for_deep_docking = len(dl_lines)
            
            print(f'Total ligand links: {total_links}')
            print(f'Total ligand links for trainingset: {links_for_vina_docking}')
            print(f'Total ligand links for testset: {links_for_deep_docking}')            
            
            time.sleep(3)       
            process_ligand_test(model_dir, receptor_pdb, output_model_dir, csv_path, mgl_directory, max_workers, vina_lines)

            # Descriptors calculation
            print("\nTraining set docking is done, the next is descriptors calculation")
            ask_to_continue()                       
            getinput_dir = os.path.join(output_model_dir, 'ldd_result')
            os.makedirs(getinput_dir, exist_ok=True)

            getoutput_dir = os.path.join(output_model_dir, 'ldd_result')
            os.makedirs(getoutput_dir, exist_ok=True)            
            
            time.sleep(4)
            output_file = prepareData(csv_path, getinput_dir, getoutput_dir)
            df = pd.read_csv(output_file)

            # Generate model
            print("\nTraining set descriptors calculation is done, the next is generating deep model")
            ask_to_continue()
            time.sleep(5)
            mode, model_output_path = generate_model(df, getoutput_dir, lismode, act_log, act_plot, transformX, transformY, scalerX, scalerY, ephocs, dense_units, batch_size, columns_to_remove, all_features, activity, model_dir_name, output_file)
            
            print(f'mode:{mode}')
            print(f'model_output_path: {model_output_path}')
            
            # Deep Docking
            print("\nGenerating deep model is done, the next is testset deep score calculation")
            ask_to_continue()
            time.sleep(6)            
            output_csv = testing_model(model_output_path, dl_lines, getoutput_dir, mode, model_dir_name)
            sort_and_add_number(output_csv, 'deep_score')         
            
            print(f"\nSuccess: {model_dir_name.upper()}")
            os.chdir(current_dir)
    
        elif receptor_pdb is None or reference_pdb is None:
            print(f"\nSkipping {model_dir_name}: receptor or reference file not found")
            os.chdir(current_dir)
    
    # Print developer's note, contact, and citation listdir
    print_dev(developer_note, developer_contact, citation_list)

if __name__ == "__main__":    
    current_dir = (os.path.join(os.getcwd(), "ladeepdock"))
    if os.path.exists(current_dir):
        main()
        run_simulation()
    else:
        print("Your job directory is not ready. Please create it using:")
        print("ladock --create ladeepdock")
