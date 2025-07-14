import numpy as np
import pandas as pd
import os

def get_database_material(idx):
    """
    Retrieves the material name and absorption coefficients from a CSV file based on the given index.
    The CSV file is expected to be in the current working directory and named "materials.csv".

    Parameters
    ----------
    idx : int
        The index of the material in the CSV file.

    Returns
    -------
    tuple
        A tuple containing the material name material_name (str) and an array of absorption coefficients abs_coeff (np.ndarray).
        The absorption coefficients are expected to be in the columns 1 to 8 of the CSV file.
    """

    path = os.getcwd()
    df = pd.read_csv(os.path.join(path, "materials.csv"))
    material_name = df.iloc[idx, 0]
    abs_coeff = df.iloc[idx, [1, 2, 3, 4, 5, 6, 7, 8]].to_numpy(dtype=float)

    return material_name,abs_coeff
