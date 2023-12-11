# v. 8.5.0 231123

import logging
#import logging.config
import os
import argparse
import sys
import logging
import pandas as pd
import math
import random
import numpy as np
from psutil import subprocess
from datetime import datetime

SAROOT = os.path.dirname(os.path.abspath(__file__))
sa_scripts_demo=SAROOT + '/demo'
sys.path.append(sa_scripts_demo)

def create_demo_data(
    out_data,
    samples,
    field_separator,
    decimal_separator
    #out_log
    ):
    #basic_log_file = out_log
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(threadName)s][%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])

    logger = logging.getLogger(__name__)

    # File parameters
    filename = out_data
    num_samples = samples #10000
    logger.info('Demo data generator (target: ' + filename + ', samples: ' + str(num_samples) + ', field separator: ' + field_separator + ', decimal separator: ' + decimal_separator + '). Begin ...')
    header = ['Time(s)', 'TIME2', 'SIN', 'TRI', 'SQ', 'MIX']
    amplitude = 1.0
    frequency = 10.0
    harmonics = 10
    duty_cycle = 0.5  # For squared wave, duty cycle is the percentage of time the wave is high
    noise = 10 #% towards the amplitude

    # Initialize an empty DataFrame
    df = pd.DataFrame(columns=header)
    # Append rows to the DataFrame
    for i in range(num_samples):
        t1 = i / num_samples  # Normalize time to [0, 1]
        t2 = t1
        s1 = sin_wave(t1, amplitude, frequency, noise)
        s2 = triangular_wave(t1, amplitude, frequency, noise)
        s3 = squared_wave(t1, amplitude, frequency, noise, duty_cycle)
        s4 = mix_sin_wave(t1, amplitude, (0, 100), 20, noise, 30)

        # Append a new row to the DataFrame
        df = pd.concat([df, pd.DataFrame({header[0]: [t1], header[1]: [t2], header[2]: [s1], header[3]: [s2], header[4]: [s3], header[5]: [s4]})], ignore_index=True)

    # Save DataFrame to CSV with custom separators and formatted numbers
    df.to_csv(filename, sep=field_separator, index=False, float_format=f'%.6f', decimal=decimal_separator)

    logger.info(f'Demo data file "{filename}" created successfully.')
    return filename

def process_data(process_script, data_file):
    logger = logging.getLogger(__name__)
    this_script_path = os.path.dirname(os.path.abspath(__file__))

    out_dir = datetime.now().strftime('./demo_%Y%m%d%H%M%S')
    if not os.path.exists(out_dir):
        # If it doesn't exist, create the directory
        os.makedirs(out_dir)
        logger.info('Output directory created: ' + out_dir)
    pdata_command = ['python', os.path.abspath(this_script_path + '/../' + process_script), '--qplot', 'Time(s)', 'SIN', 'TRI', 'SQ', 'MIX', '--include-histogram', '--dedicated-tab', '3dspctg', '--include-3d-spectrogram', '--include-wl-transform', '--input-path', data_file, '--remove-dc-offset', '--out-directory', out_dir, '--poly-int', '5:0.1,0.3', '3:0.6,0.62', '--frequency-filter', ',-35', '35,']

    subprocess.run(pdata_command)
    logger.info('\n\nDEMO POST-EXECUTION SUMMARY:\n\n1. An artificial data file was created to feed this demo: ' + data_file +
                '\n\n2. The data file was processed, proper plots displayed, and output data saved to: ' + out_dir +
                '\n\nNOTE: the command you would need to launch, in order to create the same output and behavior, is:\n' + ' '.join(pdata_command))

def gaussian_decay(frequencies, center_frequency, spread_factor):
    return np.exp(-(frequencies - center_frequency)**2 / (2 * spread_factor**2))

# Function to generate a mix sin wave with random noise
def mix_sin_wave(t, amplitude, frequency_interval, harmonics, noise_pct, spread_factor):
    abs_noise = amplitude * (1 + (noise_pct / 100))
    noise = random.uniform(-abs_noise, abs_noise)
    frequencies = np.linspace(frequency_interval[0], frequency_interval[1], harmonics)
    amplitudes = gaussian_decay(frequencies, np.mean(frequency_interval), spread_factor)
    result = np.sum(amplitudes * np.sin(2 * np.pi * frequencies * t)) + abs_noise
    return result
    
def mix_sin_waveold(t, amplitude, harmonics, frequency, noise_pct):
    ret = 0
    for i in range(1, harmonics):
         ret = ret + sin_wave(t, amplitude, harmonics * frequency, noise_pct)
    return ret

def sin_wave(t, amplitude, frequency, noise_pct):
    abs_noise = amplitude * noise_pct / 100
    noise = random.uniform(-abs_noise, abs_noise)
    return amplitude * math.sin(2 * math.pi * frequency * t) + noise

# Function to generate a triangular wave with random noise
def triangular_wave(t, amplitude, frequency, noise_pct):
    abs_noise = amplitude * noise_pct / 100
    noise = random.uniform(-abs_noise, abs_noise)
    return 2 * amplitude * (frequency * t - math.floor(frequency * t + 0.5)) + noise

# Function to generate a squared wave with random noise
def squared_wave(t, amplitude, frequency, noise_pct, duty_cycle):
    abs_noise = amplitude * noise_pct / 100
    noise = random.uniform(-abs_noise, abs_noise)
    return amplitude * ((frequency * t) % 1 < duty_cycle) + noise

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out-data', type=str, default='./demo-data.csv', help='This file will be created with three waves to analyze')
    parser.add_argument('--samples', type=int, default=1000, help='Number of samples')
    parser.add_argument('--field-separator', type=str, default=',', help='Field separator')
    parser.add_argument('--decimal-separator', type=str, default='.', help='Decimal point separator')
    #parser.add_argument('--out-log', type=str, default='./wavecracker-demo.log', help='Log file')
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = parse_opt()
    data_file = create_demo_data(**vars(opt))
    process_data('signalanalyzer.py', data_file)
