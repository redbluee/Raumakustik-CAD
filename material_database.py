import numpy as np
import pandas as pd
import os

def get_database_material(idx):

    path = os.getcwd()
    df = pd.read_csv(os.path.join(path, "materials.csv"))
    material_name = df.iloc[idx, 0]
    abs_coeff = df.iloc[idx, [1, 2, 3, 4, 5, 6, 7, 8]].to_numpy(dtype=float)

    return material_name,abs_coeff