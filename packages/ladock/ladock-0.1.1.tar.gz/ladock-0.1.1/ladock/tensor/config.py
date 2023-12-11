# simulation parameter setting
config_file_path = 'tensorConfig'

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
columns_to_remove = [col.strip() for col in config_values['columns_to_remove'].split(',')]
activity = config_values['activity']  # Biarkan sebagai string
act_log = config_values['act_log'].lower() == 'true'  # Konversi ke boolean
act_plot = config_values['act_plot']  # Biarkan sebagai string
transformX = config_values['transformX'].lower() == 'true'  # Konversi ke boolean
transformY = config_values['transformY'].lower() == 'true'  # Konversi ke boolean
scalerX = config_values['scalerX']  # Biarkan sebagai string
scalerY = config_values['scalerY']  # Biarkan sebagai string
all_features = config_values['all_features']  # Biarkan sebagai string
ephocs = int(config_values['ephocs'])
batch_size = int(config_values['batch_size'])
dense_units = config_values['dense_units']  # Biarkan sebagai string
optimizer = config_values['optimizer']  # Biarkan sebagai string
