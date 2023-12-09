import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, AllChem, MACCSkeys, rdmolops
from rdkit.Chem.rdReducedGraphs import GetErGFingerprint
from rdkit.Chem.Descriptors3D import CalcMolDescriptors3D
from rdkit.Avalon import pyAvalonTools
from rdkit.Chem.TorsionFingerprints import (
    CalculateTFD, CalculateTorsionAngles, CalculateTorsionLists,
    CalculateTorsionWeights, GetBestTFDBetweenMolecules,
    GetTFDBetweenConformers, GetTFDBetweenMolecules, GetTFDMatrix
)
import numpy as np
import pandas as pd

def get_2d_descriptors(mol, smiles, missing_val=None):
    descriptors_2d = {}
    mol = rdkit.Chem.MolFromSmiles(smiles)
    if mol is not None:      
        try:
            for desc_name, fn in Descriptors.descList:
                val = fn(mol)
                descriptors_2d[desc_name] = val
            
        except Exception as e:
            print(f"Error calculating 2D descriptors for: {smiles}")
            descriptors_2d = {desc_name: missing_val for desc_name, _ in Descriptors.descList}
    else:
        descriptors_2d = {desc_name: missing_val for desc_name, _ in Descriptors.descList}
        print(f"Molecule is None for smiles: {smiles}")

    return descriptors_2d
    
def get_3d_descriptors(mol, smiles):
    descriptors_3d = {}    
    
    if mol is not None:
        try:
            descriptors_3d = CalcMolDescriptors3D(mol)
            
        except Exception as e:
            print(f"Error calculating 3D descriptors for: {smiles}")
            descriptors_3d = {}
    
    else:
        print(f"Molecule is None for smiles: {smiles}")
        descriptors_3d = {}            
    return descriptors_3d
     
def get_lipinski_descriptors(mol, smiles):
    descriptors_lipinski = {}

    if mol is not None:
        try:

            descriptors_lipinski = {
                'FractionCSP3': Lipinski.FractionCSP3(mol),
                'HeavyAtomCount': Lipinski.HeavyAtomCount(mol),
                'NHOHCount': Lipinski.NHOHCount(mol),
                'NOCount': Lipinski.NOCount(mol),
                'NumAliphaticCarbocycles': Lipinski.NumAliphaticCarbocycles(mol),
                'NumAliphaticHeterocycles': Lipinski.NumAliphaticHeterocycles(mol),
                'NumAliphaticRings': Lipinski.NumAliphaticRings(mol),
                'NumAromaticCarbocycles': Lipinski.NumAromaticCarbocycles(mol),
                'NumAromaticHeterocycles': Lipinski.NumAromaticHeterocycles(mol),
                'NumAromaticRings': Lipinski.NumAromaticRings(mol),
                'NumHAcceptors': Lipinski.NumHAcceptors(mol),
                'NumHDonors': Lipinski.NumHDonors(mol),
                'NumHeteroatoms': Lipinski.NumHeteroatoms(mol),
                'NumRotatableBonds': Lipinski.NumRotatableBonds(mol),
                'NumSaturatedCarbocycles': Lipinski.NumSaturatedCarbocycles(mol),
                'NumSaturatedHeterocycles': Lipinski.NumSaturatedHeterocycles(mol),
                'NumSaturatedRings': Lipinski.NumSaturatedRings(mol),
                'RingCount': Lipinski.RingCount(mol),
            }

            for desc_name, desc_value in descriptors_lipinski.items():
                pass

        except Exception as e:
            print(f"Error calculating Lipinski descriptors for: {smiles}")
            descriptors_lipinski = {}

    else:
        print(f"Molecule is None for smiles: {smiles}")
        descriptors_lipinski = {}

    return descriptors_lipinski
     
def get_morgan_fp_descriptors(mol, smiles):    
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    return [int(bit) for bit in fp]

def get_maccs_fp_descriptors(mol, smiles):    
    fp = MACCSkeys.GenMACCSKeys(mol)
    return [int(bit) for bit in fp]
    
def get_daylight_fp_descriptors(mol, smiles):    
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, useFeatures=True)
    return [int(bit) for bit in fp]

def get_avalon_fp_descriptors(mol, smiles):    
    fp = pyAvalonTools.GetAvalonFP(mol)
    return [int(bit) for bit in fp] 

def get_tt_fp_descriptors(mol, smiles):    
    fp = AllChem.GetHashedTopologicalTorsionFingerprintAsBitVect(mol)
    return [int(bit) for bit in fp] 

def get_pubchem_fp_descriptors(mol, smiles):    
    fp = rdmolops.PatternFingerprint(mol)
    return [int(bit) for bit in fp]


