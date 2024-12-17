# Kraken2Polute

This repository contains a Bash script for processing paired-end sequencing data using Kraken2, a taxonomic sequence classifier. The script automates the steps of activating a Conda environment, processing sequencing files, and generating reports.

## Prerequisites

- **Mamba**: A fast alternative to Conda for package management.
- **Kraken2**: Ensure Kraken2 is installed in your Conda environment.

## Installation

1. **Install Mamba** (if not already installed):
   ```bash
   conda install mamba -n base -c conda-forge
   ```

2. **Create a Conda environment with Kraken2**:
   ```bash
   mamba create -n kraken2 -c bioconda kraken2
   ```

3. **Activate the environment**:
   ```bash
   conda activate kraken2
   ```

4. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd Kraken2Polute
   ```

5. **Make the script executable**:
   ```bash
   chmod +x kraken2_processing.sh
   ```

## Usage

Run the script with optional parameters:

```bash
./kraken2_processing.sh [options]
```

### Options

- `-i, --input-dir`: Input directory containing subdirectories with sequencing files (default: `Run2_trim`)
- `-o, --output-dir`: Output directory to save results (default: `Run4_pollute`)
- `-d, --db-path`: Path to Kraken2 database (default: `/home/maolp/data5/All_zhuyue_inluolab/kdb`)
- `-t, --threads`: Number of threads to use (default: `8`)
- `-e, --conda-env`: Conda environment to activate (default: `kraken2`)
- `-h, --help`: Display help message

### Example

```bash
./kraken2_processing.sh -i my_input_dir -o my_output_dir -d /path/to/kraken_db
```

## plots

Then run the script using the command line with the following options:

```bash
python Kraken2Polute_plots.py -i <input_directory> -o <output_directory> -t <threshold>
```

### Arguments

- `-i`, `--input_dir`: The directory containing `.kraken.report` files. Default is `Run4_pollute`.
- `-o`, `--output_dir`: The directory where the generated pie chart figures will be saved. Default is `Plots`.
- `-t`, `--threshold`: The percentage threshold for merging small classifications into an "Others" category. Default is `1.0`.

### Example

```bash
python script_name.py -i my_reports -o my_charts -t 0.5
```


