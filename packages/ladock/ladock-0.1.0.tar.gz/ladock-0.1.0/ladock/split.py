from rdkit import Chem
import os

def split_sdf_file(input_file, output_dir, molecules_per_file=500):
    print(input_file)
    suppl = Chem.SDMolSupplier(input_file)

    total_molecules = len(suppl)
    total_files = total_molecules // molecules_per_file + 1

    if total_molecules >= molecules_per_file:
        for file_num, start_idx in enumerate(range(0, total_molecules, molecules_per_file)):
            end_idx = start_idx + molecules_per_file

            output_file = os.path.join(output_dir, f"output_{file_num + 1}.sdf")
            with Chem.SDWriter(output_file) as writer:
                for mol_idx in range(start_idx, min(end_idx, total_molecules)):
                    mol = suppl[mol_idx]
                    if mol is not None:
                        writer.write(mol)
            print(f"Successfully split {input_file} into {output_file}")

    else:
        # Jika jumlah molekul kurang dari batas per file, salin saja file ke direktori output
        output_file = os.path.join(output_dir, "output_1.sdf")
        with Chem.SDWriter(output_file) as writer:
            for mol in suppl:
                if mol is not None:
                    writer.write(mol)
        print(f"Successfully copied {input_file} to {output_file}")

def split_smiles_file(input_file, output_dir, lines_per_file=100):
    print(f"Input file: {input_file}")
    
    if not os.path.isfile(input_file):
        print("Error: Input file not found.")
        return
    
    with open(input_file, 'r') as file:
        smiles_data = file.read().splitlines()

    total_files = len(smiles_data) // lines_per_file + 1
    print(f"Total files: {total_files}, Total lines: {len(smiles_data)}")

    if total_files >= 1:
        for file_num, start_idx in enumerate(range(0, len(smiles_data), lines_per_file)):
            end_idx = start_idx + lines_per_file

            output_file = os.path.join(output_dir, f"output_{file_num + 1}.smi")
            with open(output_file, 'w') as output:
                for smiles_line in smiles_data[start_idx:end_idx]:
                    output.write(smiles_line + '\n')
            print(f"Successfully split {input_file} into {output_file}")

    else:
        # Jika jumlah baris kurang dari batas per file, salin saja file ke direktori output
        output_file = os.path.join(output_dir, "output_1.smi")
        with open(output_file, 'w') as output:
            for smiles_line in smiles_data:
                output.write(smiles_line + '\n')
        print(f"Successfully copied {input_file} to {output_file}")

