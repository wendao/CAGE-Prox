#!/usr/bin/env python3
"""
PDB Atom Reordering Tool

This script takes two PDB files containing the same molecule in different conformations
and with different atom orders, and reorders the atoms in the first PDB to match the
order in the second PDB file. Hydrogens are ignored in the matching process.

Usage:
    python pdb_atom_reordering.py input_pdb reference_pdb output_pdb

Requirements:
    - RDKit
    - NumPy
"""

import sys
import os
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem


def read_pdb(pdb_file):
    """Read a PDB file and return an RDKit molecule object."""
    mol = Chem.MolFromPDBFile(pdb_file, removeHs=False, sanitize=True)
    if mol is None:
        raise ValueError(f"Could not parse PDB file: {pdb_file}")
    return mol


def get_atom_mapping(mol1, mol2):
    """
    Find the mapping between atoms in mol1 and mol2 based on chemical identity.
    Returns a dictionary mapping atom indices from mol1 to mol2.
    """
    # Get SMILES with atom mapping indices for both molecules
    mol1_no_h = Chem.RemoveHs(mol1)
    mol2_no_h = Chem.RemoveHs(mol2)
    
    # Create canonical SMILES with atom indices for both molecules
    mol1_atoms = {}
    for atom in mol1_no_h.GetAtoms():
        atom.SetProp("molAtomMapNumber", str(atom.GetIdx()))
    
    mol2_atoms = {}
    for atom in mol2_no_h.GetAtoms():
        atom.SetProp("molAtomMapNumber", str(atom.GetIdx()))
    
    # Get the SMILES with atom mapping
    smiles1 = Chem.MolToSmiles(mol1_no_h, isomericSmiles=True)
    smiles2 = Chem.MolToSmiles(mol2_no_h, isomericSmiles=True)
    
    # Create a common template molecule from the canonical SMILES
    template = Chem.MolFromSmiles(Chem.CanonSmiles(smiles1))
    
    # Match both molecules to the template
    matches1 = mol1_no_h.GetSubstructMatches(template, uniquify=False)
    matches2 = mol2_no_h.GetSubstructMatches(template, uniquify=False)
    
    if not matches1 or not matches2:
        raise ValueError("Could not match molecules - they may be different")
    
    # Use the first match (should be the best one)
    match1 = matches1[0]
    match2 = matches2[0]
    
    # Create mapping from mol1 to mol2 atoms
    mapping = {}
    for i, j in zip(match1, match2):
        mapping[i] = j
    
    # Create mapping back to original molecules with hydrogens
    original_mapping = {}
    
    # Map from mol1 (with H) to mol1_no_h indices
    mol1_to_no_h = {}
    orig_atoms = [a for a in mol1.GetAtoms() if a.GetAtomicNum() != 1]
    no_h_atoms = [a for a in mol1_no_h.GetAtoms()]
    
    for i, atom in enumerate(orig_atoms):
        if i < len(no_h_atoms):
            mol1_to_no_h[atom.GetIdx()] = i
    
    # Map from mol2_no_h indices to mol2 (with H) indices
    no_h_to_mol2 = {}
    orig_atoms = [a for a in mol2.GetAtoms() if a.GetAtomicNum() != 1]
    no_h_atoms = [a for a in mol2_no_h.GetAtoms()]
    
    for i, atom in enumerate(orig_atoms):
        if i < len(no_h_atoms):
            no_h_to_mol2[i] = atom.GetIdx()
    
    # Create the final mapping
    for atom_idx in mol1_to_no_h:
        no_h_idx = mol1_to_no_h[atom_idx]
        if no_h_idx in mapping:
            mapped_no_h_idx = mapping[no_h_idx]
            if mapped_no_h_idx in no_h_to_mol2:
                original_mapping[atom_idx] = no_h_to_mol2[mapped_no_h_idx]
    
    return original_mapping


def reorder_pdb(input_pdb, reference_pdb, output_pdb):
    """
    Reorder atoms in the input PDB file to match the atom order in the reference PDB file.
    """
    print(f"Reading input PDB: {input_pdb}")
    input_mol = read_pdb(input_pdb)
    
    print(f"Reading reference PDB: {reference_pdb}")
    ref_mol = read_pdb(reference_pdb)
    
    print("Computing atom mapping between molecules...")
    atom_mapping = get_atom_mapping(input_mol, ref_mol)
    
    # Read the original PDB content
    with open(input_pdb, 'r') as f:
        pdb_lines = f.readlines()
    
    # Extract ATOM/HETATM lines and other lines
    atom_lines = []
    other_lines = []
    
    for line in pdb_lines:
        if line.startswith("ATOM  ") or line.startswith("HETATM"):
            atom_lines.append(line)
        else:
            other_lines.append(line)
    
    # Create a new PDB with reordered atoms
    new_atom_lines = [""] * len(atom_mapping)
    
    # Dictionary to track atoms that have been matched
    matched_atoms = set()
    
    for input_idx, ref_idx in atom_mapping.items():
        if input_idx < len(atom_lines):
            # Get atom line from input PDB
            atom_line = atom_lines[input_idx]
            
            # Use atom name from reference molecule
            ref_atom = ref_mol.GetAtomWithIdx(ref_idx)
            ref_atom_name = ref_atom.GetPDBResidueInfo().GetName().strip()
            
            # Update the atom name in the PDB line (columns 13-16)
            new_line = atom_line[:12] + f"{ref_atom_name:>4}" + atom_line[16:]
            
            # Store the reordered line
            if ref_idx < len(new_atom_lines):
                new_atom_lines[ref_idx] = new_line
                matched_atoms.add(input_idx)
    
    # Add any unmatched atoms (like hydrogens) at the end
    unmatched_atoms = []
    for i, line in enumerate(atom_lines):
        if i not in matched_atoms:
            unmatched_atoms.append(line)
    
    # Filter out empty lines from new_atom_lines
    new_atom_lines = [line for line in new_atom_lines if line]
    
    # Write the new PDB file
    with open(output_pdb, 'w') as f:
        # Write header lines
        for line in other_lines:
            if not (line.startswith("END") or line.startswith("CONECT")):
                f.write(line)
        
        # Write reordered atom lines
        for i, line in enumerate(new_atom_lines):
            # Update atom serial number (columns 7-11)
            serial_num = i + 1
            new_line = "HETATM" + f"{serial_num:5d}" + line[11:]
            f.write(new_line)
        
        # Write unmatched atoms
        start_idx = len(new_atom_lines) + 1
        for i, line in enumerate(unmatched_atoms):
            serial_num = start_idx + i
            new_line = line[:6] + f"{serial_num:5d}" + line[11:]
            f.write(new_line)
        
        # Write footer lines
        for line in other_lines:
            if line.startswith("END") or line.startswith("CONECT"):
                f.write(line)


def main():
    if len(sys.argv) != 4:
        print("Usage: python pdb_atom_reordering.py input_pdb reference_pdb output_pdb")
        sys.exit(1)
    
    input_pdb = sys.argv[1]
    reference_pdb = sys.argv[2]
    output_pdb = sys.argv[3]
    
    try:
        reorder_pdb(input_pdb, reference_pdb, output_pdb)
        print(f"Successfully wrote reordered PDB to: {output_pdb}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
