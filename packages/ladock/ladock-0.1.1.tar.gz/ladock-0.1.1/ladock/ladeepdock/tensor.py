from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer, PowerTransformer, RobustScaler, PolynomialFeatures
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow import keras
from itertools import combinations
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error
import os
import glob
from ladock.ladeepdock.config import lismode, activity, columns_to_remove, act_log, act_plot, transformX, transformY, scalerX, scalerY, ephocs, batch_size, dense_units, optimizer, all_features

from datetime import datetime

def save_log(output_dir, basename, execution_time, mode, df_file, activity, columns_to_remove,
             act_log, act_plot, transformX, transformY, scalerX, scalerY,
             X_test, X_train, r2_test, mae_test, r2_train, mae_train,
             model_output_path, output_plot_file_path, output_loss_plot_path,
             ephocs, optimizer, X_features):

    log_output_path = os.path.join(output_dir, f'{basename}_{mode}_tensor.log')
    
    with open(log_output_path, 'w') as log_file:  
        model_creation_code = (
            "model = Sequential([\n"
            f"    keras.layers.Input(shape=({X_train.shape[1]},)),\n"
        )
        model_creation_code += "".join([f"    Dense({units}, activation='relu'),\n" for units in dense_units])
        model_creation_code += "    Dense(1)\n])\n"
    
    with open(log_output_path, 'w') as log_file:
        log_file.write(f'Execution Time: {execution_time}\n')
        log_file.write(f'Mode(mode): {mode}\n')
        log_file.write(f'File data input: {df_file}\n')
        log_file.write(f'Activity columns(activity): {activity}\n')
        log_file.write(f'Columns to remove (columns_to_remove): {columns_to_remove}\n')
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
        log_file.write(f'Plot saved to {output_plot_file_path}\n')
        log_file.write(f'Loss plot saved to {output_loss_plot_path}\n')
        log_file.write("Model Creation Code:\n")
        log_file.write(model_creation_code)
        log_file.write(f'Ephocs: {ephocs}\n')
        log_file.write(f'optimizer: {optimizer}\n')
        log_file.write(f'Features:\n')
        log_file.write(f', '.join(X_features))



def generate_model(lismode, act_log, act_plot, transformX, transformY, scalerX, scalerY, ephocs, dense_units, batch_size, columns_to_remove, all_features, activity, csv_file):
    modes = lismode.split(', ')
    model_output_path = None

    for mode in modes:
        execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'Mode: {mode.upper()}\n')

        # Buat direktori input dan output
        current_dir = os.getcwd()
        input_dir = os.path.join(current_dir, 'tensor_input')
        output_dir = os.path.join(current_dir, 'tensor_output')

        # Buat pola nama file yang mengandung mode
        file_pattern = f'*.csv'
        df_files = glob.glob(os.path.join(input_dir, file_pattern))

        for df_file in df_files:
            df = pd.read_csv(df_file)
            print(df)
            basename = os.path.splitext(os.path.basename(df_file))[0]

            # Hapus nilai-nilai yang hilang (NaN)
            if df.empty:
                print("Error: No data points remaining after dropping NaN values.")
            else:
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

                # Check if there are any data points remaining after dropping columns
                if X_features.empty:
                    print("Error: No data points remaining after dropping columns.")
                else:
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

                    # Generate and train model with Keras
                    dense_units = [int(unit) for unit in dense_units.split(",")]

                    # Create and compile the model
                    model = Sequential([
                        Dense(units, activation='relu') for units in dense_units
                    ] + [Dense(1)])  # Assuming you're doing a regression task

                    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)  # Adjust the learning rate if needed
                    model.compile(optimizer=optimizer, loss='mean_squared_error')

                    # Training with early stopping
                    callback = EarlyStopping(monitor='val_loss', patience=100, verbose=1)
                    history = model.fit(X_train, y_train, epochs=ephocs, batch_size=batch_size, validation_data=(X_test, y_test), callbacks=[callback])

                    # Predict on the test data
                    y_test_pred = model.predict(X_test)
                    y_train_pred = model.predict(X_train)

                    # Convert the normalized predictions back to the original scale
                    if transformY:
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
                    lim_down = min(np.min(Ytest), np.min(Ytrain)) - 0.2 * abs(max(np.max(Ytest), np.max(Ytrain)) - min(np.min(Ytest), np.min(Ytrain)))
                    lim_up = max(np.max(Ytest), np.max(Ytrain)) + 0.2 * abs(max(np.max(Ytest), np.max(Ytrain)) - min(np.min(Ytest), np.min(Ytrain)))
                    plt.xlim(lim_down, lim_up)
                    plt.ylim(lim_down, lim_up)

                    # Add regression lines
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

                    # Show the plot
                    print(f'Validation: R2={r2_test:.2f}, MAE={mae_test:.2f}')
                    print(f'Train: R2={r2_train:.2f}, MAE={mae_train:.2f}')

                    # Menyimpan plot ke file
                    plot_filename = f'{basename}_{mode}_tensor.png'
                    output_plot_file_path = os.path.join(output_dir, plot_filename)
                    plt.savefig(output_plot_file_path)
                    print(f'Plot disimpan sebagai {plot_filename}')

                    # Membuat plot kedua (train vs val loss)
                    plt.figure(figsize=(9, 6))
                    plt.plot(history.history['loss'], label='Train Loss')
                    plt.plot(history.history['val_loss'], label='Validation Loss')
                    plt.xlabel('Epochs')
                    plt.ylabel('Loss')

                    # Add legend
                    plt.legend()

                    # Menyimpan plot kedua ke file
                    loss_plot_filename = f'{basename}_{mode}_tensor_loss.png'
                    output_loss_plot_path = os.path.join(output_dir, loss_plot_filename)
                    plt.savefig(output_loss_plot_path)
                    print(f'Loss plot disimpan sebagai {loss_plot_filename}')

                    # Save the model to a file
                    model_filename = f'{basename}_{mode}_tensor.keras'
                    model_output_path = os.path.join(output_dir, model_filename)
                    model.save(model_output_path)
                    print(f'Model saved to {model_filename}')

                    # Simpan konfigurasi dan X_features ke file log tertentu
                    save_log(output_dir, basename, execution_time, mode, df_file, activity, columns_to_remove,
                             act_log, act_plot, transformX, transformY, scalerX, scalerY,
                             X_test, X_train, r2_test, mae_test, r2_train, mae_train,
                             model_output_path, output_plot_file_path, output_loss_plot_path,
                             ephocs, optimizer, X_features)

                    # Show the plots
                    # plt.show()

        return mode, model_output_path
