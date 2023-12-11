config_content = """# Silakan melakukan editing sesuai kebutuhan dan kenyataan Anda
# Nilai untuk -bt (box type):
box_type = triclinic

# Nilai untuk -d (distance)
distance = 1.2

# Nilai untuk -cs (coordinate file for solvent):
coordinate_file = spc216.gro

# Nilai untuk -rdd:
rdd = 0

# Nilai untuk -dds:
dds = 0.8

# This directory structure has been created using LADOCK. Follow these steps to prepare your input files and execute the simulations:

# 1. Place each receptor and ligand(s) (separate files) in the each "complex" directory.
# 2. Make necessary edits to the mdp files in the job directory (LADOCK_gmxprolig) as needed.
# 3. Ensure that receptor file in .pdb format (rec_*.pdb).
# 4. Ensure that ligand file(s) in .pdb format (lig_*.pdb).
# 5. Adjust the parameters in the 'config_gmxprolig.txt' file in the job directory as needed.
# 6. Execute the following command: "ladock --run gmxprolig" to run the simulation.
"""

