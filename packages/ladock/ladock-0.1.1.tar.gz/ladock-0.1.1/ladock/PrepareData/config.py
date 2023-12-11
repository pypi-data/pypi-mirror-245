import os
import glob

# simulation parameter setting
current_dir = os.getcwd()
config_file_path = os.path.join(current_dir, 'preparedataConfig')

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

# Mengakses nilai variabel
lismode = config_values['lismode']
geom = config_values['geom']
num_conformers = int(config_values['num_conformers'])
maxIters = int(config_values['maxIters'])
input_column = config_values['input_column']

mode_2d = ["2d", "lipinski", "morgan_fp"]
mode_3d = ["3d"] 
mode_fp = ["maccs_fp", "daylight_fp", "tt_fp", "avalon_fp", "pubchem_fp"]
