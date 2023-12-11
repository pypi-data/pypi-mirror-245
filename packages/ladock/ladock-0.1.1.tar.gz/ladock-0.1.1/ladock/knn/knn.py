from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer, PowerTransformer, RobustScaler, PolynomialFeatures
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from datetime import datetime
from config import lismode, activity, columns_to_remove, k_neighbors, act_log, act_plot, transformX, transformY, scalerX, scalerY, all_features

# Calculation descriptor by modes
modes = lismode.split(', ')

for mode in modes:
    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'Mode: {mode.upper()}\n')
    
    # Buat direktori input dan output
    current_dir = os.getcwd()
    input_dir = os.path.join(current_dir, 'knn_input')
    output_dir = os.path.join(current_dir, 'knn_output')

    # Buat pola nama file yang mengandung mode
    file_pattern = f'*{mode}*.csv'
    df_files = glob.glob(os.path.join(input_dir, file_pattern))    
    for df_file in df_files:
        df = pd.read_csv(df_file)
        basename = os.path.splitext(os.path.basename(df_file))[0]
        
    # Hapus nilai-nilai yang hilang (NaN)
    df = df.dropna()

    # Convert IC50 to pIC50
    if act_log:        
        actplot = f'p{act_plot}'
        act = f'p{act_plot}'
        df[act] = -np.log10(df[activity] * 1e-9)
    else:
    	actplot = act_plot
    	act = activity
    
    # Split features X and target Y
    columns_to_remove = [col.strip() for col in columns_to_remove]
    columns_to_remove.append(act)     
    X_features = df.drop(columns=columns_to_remove, axis=1)
    y = df[act]
    # Initialize scalers
    if scalerX == 'StandardScaler':
        scaler_X = StandardScaler()
    elif scalerX == 'RobustScaler':
        scaler_X = RobustScaler()
    elif scalerX == 'MinMaxScaler':
        scaler_X = MinMaxScaler()
    elif scalerX == 'Normalizer':
        scaler_X = Normalizer()
        
    if scalerY == 'StandardScaler':
        scaler_y = StandardScaler()
    elif scalerY == 'RobustScaler':
        scaler_y = RobustScaler()
    elif scalerY == 'MinMaxScaler':
        scaler_y = MinMaxScaler()
    elif scalerY == 'Normalizer':
        scaler_y = Normalizer()

    # Transform data  
    if transformY:
        y_normalized = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()
    else:
        y_normalized = y

    if transformX:
        X_normalized = scaler_X.fit_transform(X_features)
    else:
        X_normalized = X_features

    # Split the data into training and testing sets
    if all_features:
        X_train, X_test, y_train, y_test = train_test_split(X_normalized, y_normalized, test_size=0.2, random_state=1)
    else:
        feature_list = X_features.columns
        feature_indices = [X_features.columns.get_loc(feature) for feature in feature_list]
        X_train, X_test, y_train, y_test = train_test_split(X_normalized[:, feature_indices], y_normalized, test_size=0.2, random_state=1)

    # Initialize the K-Nearest Neighbors model
    model = KNeighborsRegressor(n_neighbors=k_neighbors)

    # Train the model
    model.fit(X_train, y_train)

    # Predictions on the training and test sets
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Evaluate the model on the training set
    train_mse = mean_squared_error(y_train, y_train_pred)
    print(f"Train MSE: {train_mse:.4f}")

    # Evaluate the model on the test set
    test_mse = mean_squared_error(y_test, y_test_pred)
    print(f"Test MSE: {test_mse:.4f}")

    # Convert the normalized predictions back to the original scale
    if transformX:
        y_test_pred_original_scale = scaler_y.inverse_transform(y_test_pred.reshape(-1, 1)).flatten()
        y_train_pred_original_scale = scaler_y.inverse_transform(y_train_pred.reshape(-1, 1)).flatten()
        y_test_original_scale = scaler_y.inverse_transform(y_test.reshape(-1, 1)).flatten()
        y_train_original_scale = scaler_y.inverse_transform(y_train.reshape(-1, 1)).flatten()
    else:    
        y_test_pred_original_scale = y_test_pred.flatten()
        y_train_pred_original_scale = y_train_pred.flatten()
        y_test_original_scale = y_test
        y_train_original_scale = y_train

    # Plot y vs. y_calculate
    plt.figure(figsize=(9, 9))
    plt.scatter(y_test_original_scale, y_test_pred_original_scale, alpha=0.5, label=f'Validation Data: {len(X_test)} molecules')
    plt.scatter(y_train_original_scale, y_train_pred_original_scale, alpha=0.5, label=f'Train Data: {len(X_train)} molecules')

    # Add labels to the axes
    plt.xlabel(f'True {actplot}')
    plt.ylabel(f'Predicted {actplot}')

    # Set consistent axis limits
    Ytest = y_test_original_scale
    Ytrain = y_train_original_scale
    lim_down = min(np.min(Ytest), np.min(Ytrain)) - 0.1 * abs(max(np.max(Ytest), np.max(Ytrain)) - min(np.min(Ytest), np.min(Ytrain)))
    lim_up = max(np.max(Ytest), np.max(Ytrain)) + 0.1 * abs(max(np.max(Ytest), np.max(Ytrain)) - min(np.min(Ytest), np.min(Ytrain)))
    plt.xlim(lim_down, lim_up)
    plt.ylim(lim_down, lim_up)
    
    # Add regression line
    z_test = np.polyfit(y_test_original_scale, y_test_pred_original_scale, 1)
    p_test = np.poly1d(z_test)
    z_train = np.polyfit(y_train_original_scale, y_train_pred_original_scale, 1)
    p_train = np.poly1d(z_train)

    # Calculate R-squared 
    r2_test = r2_score(y_test_original_scale, y_test_pred_original_scale)
    r2_train = r2_score(y_train_original_scale, y_train_pred_original_scale)

    # Calculate MAE 
    mae_test = mean_absolute_error(y_test_original_scale, y_test_pred_original_scale)
    mae_train = mean_absolute_error(y_train_original_scale, y_train_pred_original_scale)

    # Plot regression lines
    plt.plot(y_test_original_scale, p_test(y_test_original_scale), 'b--', label=f'Validation: R2={r2_test:.2f}, MAE={mae_test:.2f}')
    plt.plot(y_train_original_scale, p_train(y_train_original_scale), 'r--', label=f'Train: R2={r2_train:.2f}, MAE={mae_train:.2f}')

    # Add legend
    plt.legend()

    # Simpan plot ke file
    plot_file = f'{basename}_KNN.png'
    plot_output_path = os.path.join(output_dir, plot_file)
    plt.savefig(plot_output_path)
    print(f"Scatter plot saved to {plot_file}")

    # Simpan model ke file menggunakan joblib
    model_file = f'{basename}_KNN.joblib'
    model_output_path = os.path.join(output_dir, model_file)
    joblib.dump(model, model_output_path)
    print(f"KNN model saved to {model_file}")
    
    # Simpan konfigurasi dan X_features ke file log tertentu
    log_output_path = os.path.join(output_dir, f'{basename}_KNN.log')
    
    with open(log_output_path, 'w') as log_file:  
        log_file.write(f'Execution Time: {execution_time}\n')    
        log_file.write(f'Mode(mode): {mode}\n')
        log_file.write(f'File data input: {df_file}\n')
        log_file.write(f'Activity columns(activity): {activity}\n')
        log_file.write(f'Columns to remove (columns_to_remove): {columns_to_remove}\n')
        log_file.write(f'k_neighbors: {k_neighbors}\n')
        log_file.write(f'Activity Log (act_log): {act_log}\n')
        log_file.write(f'Activity label in plot: {act_plot}\n')
        log_file.write(f'Transform X: {transformX}\n')
        log_file.write(f'Transform Y: {transformY}\n')
        log_file.write(f'scalerX: {scalerX}\n')
        log_file.write(f'scalerY: {scalerY}\n')
        log_file.write(f'Validation Data: {len(X_test)} molecules\n')
        log_file.write(f'Train Data: {len(X_train)} molecules\n')
        log_file.write(f'Validation: R2={r2_test:.2f}, MAE={mae_test:.2f}\n')
        log_file.write(f'Train: R2={r2_train:.2f}, MAE={mae_train:.2f}\n')
        log_file.write(f'Model saved to {model_output_path}\n')
        log_file.write(f'Scatter plot saved to {plot_output_path}\n')
        log_file.write(f'Features:\n')
        log_file.write(f', '.join(X_features))

    # Show the plot
    plt.show()
    
