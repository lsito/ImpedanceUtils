def import_from_EM(directory, offsets, Q_factor_mode="lossy E"):  
    """
    Creates a DataFrame from EM simulations for longitudinal and transverse data
    
    Parameters:
    -----------
    directory : str
        A string with the path to the folder with results
    offsets : list
        A list of floats with the offsets that were simulated.
        They must correspond to the ones simulated.
    Q_factor_mode : str, optional (default = "lossy E")
        Choose to import "lossy E" files or "Perturbation"
    
    Returns:
    --------
    pd.DataFrame
        A DataFrame with mode number, frequency, q factor, shunt impedances.
        Each row corresponds to a mode.
    """

    fileName = r"Q-Factor (lossy E) (Multiple Modes).txt"
    df_Q = pd.read_csv(directory+fileName, sep='\t', header=None, names=['Mode', 'Q'])

    fileName = r"Frequency (Multiple Modes).txt"
    df_f = pd.read_csv(directory+fileName, sep='\t', header=None, names=['Mode', 'Frequency'])

    # Merge the two dataframes based on the 'Mode' column
    df = pd.merge(df_f, df_Q, on='Mode')

    # List all files in the directory that start with 'Shunt Impedance'
    files = [f for f in os.listdir(directory) if f.startswith("Shunt Impedance")]


    # Display the filenames
    for file, off in zip(files, offsets):
        df_R = pd.read_csv(directory+file, sep='\t', header=None, names=['Mode', f'Rs {off} mm'])
        df = pd.merge(df, df_R, on='Mode')
        
    return df