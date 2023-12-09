from rdkit import Chem
from rdkit.Chem import AllChem
from config import geom, num_conformers, maxIters

def optimize_geometry(input_data, geom=geom, num_conformers=num_conformers, maxIters=200):
    smiles, mode = input_data
    try:
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        if mol is not None:
            if mode == "2d" or mode == "lipinski" or mode == "morgan_fp":       	            	
            	return mol
            elif mode == "3d":
            	AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, randomSeed=42)
            	return mol
            else:
                AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, randomSeed=42)
                lowest_energy = float('inf')
                lowest_energy_conf_id = None

                for conf_id in range(mol.GetNumConformers()):
                    initial_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id, ignoreInterfragInteractions=False).CalcEnergy()
                    if geom == "uff":
                        AllChem.UFFOptimizeMolecule(mol, confId=conf_id, maxIters=maxIters)
                        optimized_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()
                    elif geom == "mff4":
                        AllChem.MMFFOptimizeMolecule(mol, confId=conf_id, maxIters=maxIters)
                        optimized_energy = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id).CalcEnergy()                        
                    
                    else:
                        print(f"Unsupported geometry optimization method: {geom}")
                        return None
                    
                    if optimized_energy < lowest_energy:
                        lowest_energy = optimized_energy
                        lowest_energy_conf_id = conf_id
                        optimized_molecule = mol 
                mol = optimized_molecule
                
                return mol
                          
    except Exception as e:
        print(f"Error generating and optimizing conformers for SMILES: {smiles}")
        print(f"Error details: {e}")
        return None

