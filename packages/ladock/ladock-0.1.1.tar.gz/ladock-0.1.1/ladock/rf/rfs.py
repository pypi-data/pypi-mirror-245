import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from config import labels, columns_to_remove
from datetime import datetime
import os
import glob

execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Buat direktori input dan output
current_dir = os.getcwd()
input_dir = os.path.join(current_dir, 'rf_input')
output_dir = os.path.join(current_dir, 'rf_output')

file_pattern = f'*.csv'
df_files = glob.glob(os.path.join(input_dir, file_pattern))

for df_file in df_files:
    df = pd.read_csv(df_file)
    basename = os.path.splitext(os.path.basename(df_file))[0]

    # Hapus nilai-nilai yang hilang (NaN)
    df = df.dropna()

    # Memilih fitur dan label
    features = df.drop(columns_to_remove, axis=1)
    labels = df[labels]

    # Membagi data menjadi data pelatihan dan data uji
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Standarisasi fitur (opsional, tergantung pada algoritma yang digunakan)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Inisialisasi dan melatih model klasifikasi (Random Forest sebagai contoh)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Membuat prediksi pada data uji
    y_pred = model.predict(X_test)

    # Evaluasi kinerja model
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    # Menyimpan laporan klasifikasi ke dalam file
    classification_rep = classification_report(y_test, y_pred)
    print("Classification Report:\n", classification_rep)
    classification_rep_filename = f"{basename}_classification_report.txt"
    classification_rep_output_path = os.path.join(output_dir, classification_rep_filename)
    with open(classification_rep_output_path, 'w') as rep_file:
        rep_file.write("Classification Report:\n")
        rep_file.write(classification_rep)

    print(f'Classification report saved to {classification_rep_output_path}')
    
    # Menyimpan model ke dalam direktori output
    model_filename = f"{basename}_rf.pkl"
    model_output_path = os.path.join(output_dir, model_filename)
    joblib.dump(model, model_output_path)
    print(f'Model saved to {model_output_path}')

