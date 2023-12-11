#!/usr/bin/env python
import os
import subprocess
import glob
import shutil
from datetime import datetime
from main import *

def run_pdb2gmx(receptor_files):    
    for receptor_file in receptor_files:
        rec_name = os.path.splitext(receptor_file)[0]        
        pdb2gmx_command = f'gmx pdb2gmx -f {receptor_file} -o NEW_{rec_name}.pdb -p topol_{rec_name}.top -ignh' 
      
        try:
            subprocess.run(pdb2gmx_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            pass
   
def process_mol2_files_in_directories(mol2_files):
    for mol2_file in mol2_files:
        lig_name = os.path.splitext(os.path.basename(mol2_file))[0]
        acpype_command = f'acpype -i {lig_name}.pdb -c gas'
        
        try:
            subprocess.run(acpype_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            pass

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

def create_complex_pdb(receptor_new_files, mol2_files):
    complex_data = ""
    
    try:
        for receptor_new_file in receptor_new_files:
            with open(receptor_new_file, 'r') as rec_new:
                rec_data = rec_new.read()
                complex_data += rec_data

        for mol2_file in mol2_files:
            lig_name = os.path.splitext(os.path.basename(mol2_file))[0]
            ligand_pdb = f"{lig_name}.acpype/{lig_name}_NEW.pdb"
            with open(ligand_pdb, 'r') as ligand_file:
                ligand_data = ligand_file.read()
                complex_data += ligand_data

        lines = complex_data.split('\n')
        filtered_lines = [line for line in lines if not any(keyword in line for keyword in ["TITLE", "REMARK", "MODEL", "ENDMDL"])]

        with open("complex.pdb", 'w') as output_file:
            output_file.write('\n'.join(filtered_lines))
       
    except Exception as e:
        pass

def create_complex_itp(mol2_files):
    atomtype_itp = ""    
    moleculetype_itp = ""
    complex_itp = ""
    
    for mol2_file in mol2_files:
        extract_ligand_id_from_mol2(mol2_file)            
        lig_name = os.path.splitext(mol2_file)[0]
        ligand_itp = f"{lig_name}.acpype/{lig_name}_GMX.itp"         
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
    
    # Ganti nama ligand dengan ID sesuai indeks
    for mol2_file in mol2_files:
        lig_name = os.path.splitext(mol2_file)[0]        
        lig_id = extract_ligand_id_from_mol2(mol2_file)
        complex_itp = complex_itp.replace(lig_name, lig_id)
    
    with open('ligand.itp', 'w') as complex_itp_file:
        complex_itp_file.write(complex_itp)

def split_topol2itp(topol_files):
    for topol_next in topol_files:
        atommoleculetype_lines = []
 
        write_atommoleculetype = False

        with open(topol_next, 'r') as topol_next_file:
            topol_next_lines = topol_next_file.readlines()

            for line in topol_next_lines:
                if "moleculetype" in line:
                    write_atommoleculetype = True
 
                elif "; Include water topology" in line:
                     write_atommoleculetype = False

                if write_atommoleculetype:
                    atommoleculetype_lines.append(line)

        # Simpan atommoleculetype dalam file dengan nama yang sesuai
        atommoleculetype_file_name = topol_next.replace(".top", ".itp")
        with open(atommoleculetype_file_name, 'w') as atommoleculetype_file:
            atommoleculetype_file.writelines(atommoleculetype_lines)

        # Hapus bagian atommoleculetype dan posre dari file topol_next
        with open(topol_next, 'w') as topol_next_file:
            filtered_lines = []
            remove_next = False

            for line in topol_next_lines:
                if any(keyword in line for keyword in ("moleculetype", "; Include Position restraint file")):
                    remove_next = True
                if "; Include water topology" in line:
                    remove_next = False

                if not remove_next:
                    filtered_lines.append(line)

            # Tambahkan baris yang diminta setelah baris kedua dari ; Include forcefield parameters
            index_ff_params = filtered_lines.index("; Include forcefield parameters\n")
            filtered_lines.insert(index_ff_params + 2, f"\n; Include chain topologies\n#include \"{atommoleculetype_file_name}\"\n")
            topol_next_file.writelines(filtered_lines)        

def create_topol_top(mol2_files, topol_files):

    if os.path.exists("topol.top"):
        os.remove("topol.top")
    
    if topol_files:

        top1 = topol_files[0]  # Ambil file pertama
        with open(top1, 'r') as topol_file:
            topol_lines = topol_file.readlines()

        for topol_next in topol_files[1:]:
            with open(topol_next, 'r') as topol_next:
                topol_next_lines = topol_next.readlines()
                new_topol1 = []  # Baris-baris yang dimulai dari "; Include chain topologies" hingga tidak ada lagi baris yang mengandung "#include" dari topol_next_files
                new_topol2 = []  # Semua baris setelah " ; Compound" dari topol_next_files
                
                include_chain = False
                molecules_section = False
                started_molecule_section = False

                for line in topol_next_lines:
                    if include_chain:
                        if line.startswith("#include"):
                            new_topol1.append(line)
                        else:
                            include_chain = False
                    elif line.strip() == "; Include chain topologies":
                        include_chain = True
                        
                    elif molecules_section:
                        if not started_molecule_section:
                            started_molecule_section = True
                        else:
                            new_topol2.append(line)
                    elif line.strip() == "[ molecules ]":
                        molecules_section = True
                    
                # Menambahkan new_topol1 pada topol_lines setelah "; Include chain topologies"
                if new_topol1:
                    index = topol_lines.index("; Include chain topologies\n")
                    topol_lines = topol_lines[:index + 1] + new_topol1 + topol_lines[index + 1:]

                # Menambahkan new_topol2 pada topol_lines
                if new_topol2:
                    topol_lines.extend(new_topol2)
                    
        with open("topol.top", 'w') as topol_file:
            topol_file.writelines(topol_lines)

    lig_lines1 = "; Include ligand parameters\n#include \"ligand.itp\"\n\n"
    lig_lines2= "" 
    lig_lines3 = "; Ligand position restraint\n#ifdef POSRES\n"
    lig_lines4 = ""
    lig_lines5 = "#endif\n\n" 

    for file in mol2_files:
        lig_id = extract_ligand_id_from_mol2(file)       
        lig_lines2 += f'{lig_id}\t\t\t1\n'
        lig_lines4 += f'#include "{lig_id}-posre.itp"\n'

    with open("topol.top", 'r') as topol_file:
        topol_lines = topol_file.readlines()

    index1 = None

    for i, line in enumerate(topol_lines):
        if line.strip() == "; Include forcefield parameters":
            index1 = i
            break  # Keluar dari loop setelah menemukan baris yang sesuai

    if index1 is not None:
        # Menambahkan lig_lines1 setelah baris yang sesuai
        topol_lines.insert(index1 + 3, lig_lines1)
        
        # Menambahkan lig_lines1 setelah baris yang sesuai
        topol_lines.insert(index1 + 4, lig_lines3)
        topol_lines.insert(index1 + 5, lig_lines4)
        topol_lines.insert(index1 + 6, lig_lines5)

    # Hanya menyimpan baris-baris mulai dari "; Include forcefield parameters" dan setelahnya
    index_ff_params = topol_lines.index("; Include forcefield parameters\n")
    merged_lines = topol_lines[index_ff_params:]
    
    # Menambahkan lig_lines3 pada bagian akhir
    merged_lines.extend([lig_lines2])

    # Menulis isi file topol.top yang digabungkan
    with open("topol.top", 'w') as topol_file:
        topol_file.writelines(merged_lines)
  
def generate_box_pdb(box_pdb, box_type, distance):
    command = f'gmx editconf -f complex.pdb -o {box_pdb} -bt {box_type} -d {distance} -c'
    try:        
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        pass

def solvate_system(box_pdb, spc216_gro, topol_top, solv_gro):
    command = f'gmx solvate -cp {box_pdb} -cs {spc216_gro} -p {topol_top} -o {solv_gro}'
    try:        
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        pass

def ionization(solv_gro, topol_top, ions_gro):
    grompp_cmd = f"gmx grompp -f ions.mdp -c {solv_gro} -p {topol_top} -o ions.tpr -maxwarn 1"
    genion_cmd = f"gmx genion -s ions.tpr -o {ions_gro} -p {topol_top} -pname NA -nname CL -neutral"
    try:   
        subprocess.run(grompp_cmd, shell=True)    
        subprocess.run(genion_cmd, shell=True)
    except subprocess.CalledProcessError:
        pass
    
    
def minimization(ions_gro, topol_top, rdd, dds):
    grompp_cmd = f"gmx grompp -f em.mdp -c {ions_gro} -p {topol_top} -o em.tpr -maxwarn 1"
    emrun_cmd = f"gmx mdrun -v -deffnm em -rdd {rdd} -dds {dds}"
    energy_command = f'echo "10\n0\n" | gmx energy -f em.edr -o potential.xvg'
    try:               
        subprocess.run(grompp_cmd, shell=True)
        subprocess.run(emrun_cmd, shell=True)
        subprocess.run(energy_command, shell=True)            
    except subprocess.CalledProcessError:
        pass
 
def make_index_system(em_gro, index_ndx):
    make_ndx_cmd = f"gmx make_ndx -f {em_gro} -o {index_ndx}"
    
    try:
        subprocess.run(make_ndx_cmd, shell=True)

    except subprocess.CalledProcessError:
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

def process_ligand_restraint(mol2_files):
    for mol2_file in mol2_files:
        lig_name = os.path.splitext(os.path.basename(mol2_file))[0]
        lig_id = extract_ligand_id_from_mol2(mol2_file)
        ligand_new_pdbs = glob.glob(f"{lig_name}.acpype/{lig_name}_NEW.pdb")
        
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
                
def replace_text_in_files(mol2_files):
    mdp_files = glob.glob(os.path.join(".", "*.mdp"))    
    combined_lig_id = "_".join(extract_ligand_id_from_mol2(file) for file in mol2_files)    
    for mdp_file in mdp_files:
        with open(mdp_file, 'r') as file:
            file_data = file.read()            
            file_data = file_data.replace("Protein_UNK", f"Protein_{combined_lig_id}")
        with open(mdp_file, 'w') as file:
            file.write(file_data)

def run_nvt_simulation(rdd, dds):
    grompp_cmd = f"gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 5"
    mdrun_cmd = f"gmx mdrun -v -s nvt.tpr -deffnm nvt -rdd {rdd} -dds {dds}"
    try:
        subprocess.run(grompp_cmd, shell=True, check=True)    
        subprocess.run(mdrun_cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        pass

def run_npt_simulation(rdd, dds):
    grompp_cmd = f"gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -n index.ndx -o npt.tpr -maxwarn 5"
    mdrun_cmd = f"gmx mdrun -v -s npt.tpr -deffnm npt -rdd {rdd} -dds {dds}"
    try:
        subprocess.run(grompp_cmd, shell=True, check=True)        
        subprocess.run(mdrun_cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        pass

def run_production_simulation(rdd, dds):
    grompp_cmd = f"gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md.tpr -maxwarn 5"
    mdrun_cmd = f"gmx mdrun -v -s md.tpr -deffnm md -rdd {rdd} -dds {dds}"
    try:        
        subprocess.run(grompp_cmd, shell=True, check=True)
        subprocess.run(mdrun_cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        pass


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
    with open('config_gmxprolig.txt', 'r') as config_file:
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
    rdd = config_variables['rdd']
    dds = config_variables['dds']
    current_directory = os.getcwd()  
    box_pdb = "box.pdb"    
    topol_top = "topol.top"    
    solv_gro = "solv.gro" 
    ions_gro = "ions.gro"
    em_gro = "em.gro"
    index_ndx = "index.ndx"
    
    for subdir in os.listdir(current_directory):
        if os.path.isdir(subdir):
            os.chdir(subdir)
            receptor_files = glob.glob('rec*.pdb')
            mol2_files = glob.glob('lig*.pdb')
            copy_mdp_files(current_directory, subdir)
            replace_text_in_files(mol2_files)
            process_mol2_files_in_directories(mol2_files) 
            run_pdb2gmx(receptor_files)
            topol_files = glob.glob('topol_*.top')
            receptor_new_files = glob.glob('NEW*.pdb')             
            create_complex_pdb(receptor_new_files, mol2_files)      
            create_complex_itp(mol2_files)   
            
            for topol_next in topol_files:
                with open(topol_next, 'r') as topol_next_file:
                    topol_next_lines = topol_next_file.readlines()

                    # Cek apakah topol_next_lines mengandung "moleculetype"
                    if any("moleculetype" in line for line in topol_next_lines):
                        split_topol2itp([topol_next])  # Jalankan fungsi hanya untuk file yang memenuhi syarat            
                
            create_topol_top(mol2_files, topol_files)
            generate_box_pdb(box_pdb, box_type, distance)
            solvate_system(box_pdb, spc216_gro, topol_top, solv_gro)
            ionization(solv_gro, topol_top, ions_gro)
            minimization(ions_gro, topol_top, rdd, dds)
            process_ligand_restraint(mol2_files)
            make_index_system(em_gro, index_ndx)  
            
            temp_files = glob.glob('#*')           
            for temp_file in temp_files:
                os.remove(temp_file)                        
            os.chdir('..')    
            
    for subdir in os.listdir(current_directory):
        if os.path.isdir(subdir):
            os.chdir(subdir)        
            temp_files = glob.glob('#*')  
            run_nvt_simulation(rdd, dds)
            for temp_file in temp_files:
                os.remove(temp_file)                        
            os.chdir('..')   
            run_npt_simulation(rdd, dds)
            for temp_file in temp_files:
                os.remove(temp_file)                        
            os.chdir('..')   
            run_production_simulation(rdd, dds)      
            for temp_file in temp_files:
                os.remove(temp_file)                        
            os.chdir('..')               
            
    print_dev(developer_note, developer_contact, citation_list)        
if __name__ == "__main__":
    current_directory =  (os.path.join(os.getcwd(), "LADOCK_gmxprolig"))      
    
    if os.path.exists(current_directory):
        os.chdir(current_directory)
        main() 
    else:
        print("Your job directory (LADOCK_gmxprolig) is not ready. Please create it using:")
        print("ladock --create gmxprolig")