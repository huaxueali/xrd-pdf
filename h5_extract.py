import os
import glob
import h5py
import numpy as np
import pandas as pd

def convert_h5_to_txt():
    
    os.makedirs('out', exist_ok=True)

    h5_files = glob.glob('*.h5')

    for h5_file in h5_files:
        
        with h5py.File(h5_file, 'r') as f:
            data = f['entry_0000/integrate/results/data'][:]
            data_errors = f['entry_0000/integrate/results/data_errors'][:]
            data_2theta = f['entry_0000/integrate/results/radial'][:]

        average_data = np.mean(data, axis=0)
        average_data_errors = np.mean(data_errors, axis=0)
        
        df = pd.DataFrame({'2th_deg': data_2theta, 'I': average_data, 'sigma': average_data_errors})
        
        output_file = os.path.join('out', os.path.splitext(h5_file)[0] + '.txt')
        
        df.to_csv(output_file, sep=' ', index=False)
        
if __name__ == '__main__':
    convert_h5_to_txt()