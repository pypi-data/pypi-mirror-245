# simulation parameter setting
config_file_path = 'rfConfig'

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
columns_to_remove = [col.strip() for col in config_values['columns_to_remove'].split(',')]
labels = config_values['labels']  # Biarkan sebagai string
