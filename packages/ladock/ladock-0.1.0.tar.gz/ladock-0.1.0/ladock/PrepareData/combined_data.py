import os
import pandas as pd

# Mendefinisikan direktori output dan nama file untuk setiap mode
current_dir = os.getcwd()
output_dir = os.path.join(current_dir, 'output_data', 'erbb_ok')
modes = ['2d', '3d', 'lipinski']

# Inisialisasi DataFrame kosong
df_combined = None

# Loop melalui setiap mode
for mode in modes:
    print(f'mode = {mode}')
    df_path = f'erbb_{mode}.csv'
    file_path = os.path.join(output_dir, df_path)

    # Baca DataFrame dari file CSV
    df = pd.read_csv(file_path)

    # Hapus nilai-nilai NaN jika diperlukan
    df = df.dropna()

    # Cetak kolom-kolom dan jumlah kolom dari DataFrame df
    print(f"Kolom-kolom df {mode}:")
    print(df.columns)
    print(f"Jumlah kolom: {len(df.columns)}")

    # Gabungkan DataFrame dengan DataFrame yang sudah ada berdasarkan kolom molecule_chembl_id
    if df_combined is None:
        df_combined = df
    else:
        df_combined = pd.merge(df_combined, df, on=['molecule_chembl_id', 'canonical_smiles', 'standard_value'], how='outer', suffixes=('_x', '_y'))

# Hapus baris yang memiliki nilai NaN setelah menggabungkan
df_combined = df_combined.dropna()

# Pilih kolom-kolom yang tidak memiliki sufiks '_x', '_y', atau '_z'
selected_columns = [col for col in df_combined.columns if not col.endswith(('_x', '_y', '_z'))]
df_combined = df_combined[selected_columns]

# Cetak kolom-kolom dan jumlah kolom dari DataFrame df_combined
print("Kolom-kolom df_combined:")
print(df_combined.columns)
print(f"Jumlah kolom: {len(df_combined.columns)}")

# Simpan hasil penggabungan menjadi file CSV
output_combined_path = os.path.join(output_dir, 'erbb_combined.csv')
df_combined.to_csv(output_combined_path, index=False)

# Simpan nama kolom asli ke file tertentu
columns_output_path = os.path.join(output_dir, 'columns_combined.txt')
with open(columns_output_path, 'w') as columns_file:
    columns_file.write('\n'.join(df_combined.columns))

print(f'Hasil penggabungan disimpan di: {output_combined_path}')
print(f'Nama kolom asli disimpan di: {columns_output_path}')
