# Virus Scripts

This is a repository for scripts that I am writing as a part of my virus research SIP under Dr.Wilson at Kalamazoo
College

# find_aas

This script takes in virus capsid and point array PDB files and output creates/overwrites an excel file called
\<virusname\>.xlsx
with the closest Amino Acid in the capsid to each point in the PA for each chain, along with the distance and Atom at that point, and
the nearest other AA if there is one within 5 Angstroms written to a sheet with the PA file name.

You can use the single executable file find_aas like so:

Allow it to run as an executable:

```bash
chmod +x find_aas
```

then you can call it on a single pa like so:

```bash
./find_aas 2g33.pdb pa_346.pdb
```

or you can have it loop through a directory of pa files by using the run_pas_exec.sh file

```bash
chmod +x run_pas_exec.sh
```
```bash
./run_pas_exec.sh 2g33.pdb pa_directory
```

This is a compiled executable with pyinstaller. Originally it was a python file which you can run as such with the
requirements & usage detailed below (faster).

# Requirements

scipy
pandas
numpy
openpyxl

there is a requirements.txt file so that you can install the requirements in a virtual environment like so:

first download the files or clone the git repo and cd into it

```bash
git clone https://github.com/gabeorosan/virus-scripts.git && cd virus-scripts
```

create a venv called 'myenv'
```bash
python -m venv myenv 
```
activate the environment
```bash
source myenv/bin/activate
```
and install the requirements

```bash
pip install -r requirements.txt

```

# Usage
To run (with capsid '2g33.pdb' and point array 'pa_346.pdb' in the same directory as the script):

```bash
python find_aas.py 2g33.pdb pa_346.pdb
```

There is also a run_pas.sh shell script to loop through a folder and run the above command for each point array in the folder on
a capsid (containing "pa" in the file name). To use it, first make the shell script an executable:
```bash
chmod +x run_pas.sh
```
Then call it (on capsid '2g33.pdb' for PAs in folder pa_directory)
```
./run_pas.sh 2g33.pdb pa_directory
```

# aa_plot.ipnyb

Jupyter notebook to graph some info from the excel file created by find_aas (Average distance from PA point, closest AA, other AAs)

# temp_plot.ipnyb

Notebook to graph some info from the SC_frankencode output excel file (frequency of PAs being closest, most common GPs,

# capsid_info.ipnyb

Notebook to use web apis to get various info for a given capsid

# family_stats.ipnyb

Notebook to use PDB and ViperDB web api to compile data from viruses in various families and write to families.xlsx

# family_plot.ipnyb

Notebook to average and graph some data from families.xlsx

# fold_stats.ipnyb

Notebook to get non-t1 viruses from each family (labeled with SCOP ccs) and write them to non_t_one.xlsx

# parse_scop.ipnyb

Notebook to get pdb ids from families.xlsx and their folds from scop.txt (using scop-des.txt to get the text description
for each fold id) and analyze the frequency of folds. Also created the phrenology_folds.xlsx spreadsheet with data from
    Dr.Wilson's Viral Phrenology paper and the folds of each virus.

# phrenology_plot.ipynb

Notebook to analyze the gps of viruses with different folds
