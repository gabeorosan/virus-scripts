# Virus Scripts

This is a repository for scripts that I am writing as a part of my virus research SIP under Dr.Wilson at Kalamazoo
College

# find_aas.py

This script takes in virus capsid and point array PDB files and output creates/overwrites an excel file called
\<virusname\>.xlsx
with the closest Amino Acid in the capsid to each point in the PA for each chain, along with the distance and Atom at that point, and
the nearest other AA if there is one within 5 Angstroms written to a sheet with the PA file name.

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

