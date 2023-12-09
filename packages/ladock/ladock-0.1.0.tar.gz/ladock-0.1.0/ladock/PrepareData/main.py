import os
from prepare_data import prepareData

current_dir = os.getcwd()
input_dir = os.path.join(current_dir, 'getdata_input')
output_dir = os.path.join(current_dir, 'getdata_output')

# Loop melalui setiap berkas dengan ekstensi csv di input_dir
for csv_file in os.listdir(input_dir):    
    if csv_file.endswith('.csv'):
        prepareData(csv_file, input_dir, output_dir) 

