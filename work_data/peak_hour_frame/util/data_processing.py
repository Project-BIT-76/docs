import os
import pandas as pd
import numpy as np

def save_data_to_csv(data_dict, save_dir):
    """Save data arrays to CSV files in the specified directory."""
    os.makedirs(save_dir, exist_ok=True)
    for name, data in data_dict.items():
        df = pd.DataFrame(data.reshape(data.shape[0], -1))  # Flatten except the first dimension for 2D structure
        df.to_csv(os.path.join(save_dir, f"{name}.csv"), index=False)
    print(f"Data saved to {save_dir}")

def load_data_from_csv(save_dir, data_shapes):
    """Load data arrays from CSV files and reshape according to original shapes."""
    loaded_data = {}
    for name, shape in data_shapes.items():
        file_path = os.path.join(save_dir, f"{name}.csv")
        df = pd.read_csv(file_path)
        loaded_data[name] = df.values.reshape(shape)  # Reshape to the original dimensions
    print(f"Data loaded from {save_dir}")
    return loaded_data
