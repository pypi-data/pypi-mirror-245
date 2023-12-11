import os

current_directory = os.path.join(os.getcwd(), "ladeepdock")
config_file_path = os.path.join(current_directory,'ladeepdockConfig')

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue
            key, value = map(str.strip, line.split('='))
            # Hanya ambil nilai sebelum karakter '#'
            value = value.split('#')[0].strip()
            config[key] = value
    return config

config_values = read_config(config_file_path)

# Autodock Vina model parameter setting
size_x = float(config_values.get('size_x', '40'))
size_y = float(config_values.get('size_y', '40'))
size_z = float(config_values.get('size_z', '40'))
num_modes = int(config_values.get('num_modes', '8'))
exhaustiveness = int(config_values.get('exhaustiveness', '8'))
mgl_directory = config_values.get('mgl_directory', '')

# Accessing variable values
lismode = config_values['lismode']
columns_to_remove = [col.strip() for col in config_values.get('columns_to_remove', '').split(',')]
activity = config_values.get('activity', '')  # Keep as a string
act_log = config_values.get('act_log', '').lower() == 'true'  # Convert to boolean
act_plot = config_values.get('act_plot', '')  # Keep as a string
transformX = config_values.get('transformX', '').lower() == 'true'  # Convert to boolean
transformY = config_values.get('transformY', '').lower() == 'true'  # Convert to boolean
scalerX = config_values.get('scalerX', '')  # Keep as a string
scalerY = config_values.get('scalerY', '')  # Keep as a string
all_features = config_values.get('all_features', '')  # Keep as a string
ephocs = int(config_values.get('ephocs', '0'))
batch_size = int(config_values.get('batch_size', '0'))
dense_units = [int(unit) for unit in config_values.get('dense_units', '').split(",")]  # Convert to a list of integers
optimizer = config_values.get('optimizer', '')  # Keep as a string

# Prepare data parameter setting
geom = config_values.get('geom', 'uff')  # Other option for geometry optimization: mff4, uff
num_conformers = int(config_values.get('num_conformers', '20'))  # Conformation numbers when geometry optimization of molecules
maxIters = int(config_values.get('maxIters', '500'))  # Maximum amount of iteration when geometry optimization of molecules
input_column = config_values.get('input_column', 'smiles')

mode_2d = ["2d", "lipinski", "morgan_fp"]
mode_3d = ["3d"] 
mode_fp = ["maccs_fp", "daylight_fp", "tt_fp", "avalon_fp", "pubchem_fp"]
