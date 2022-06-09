# Virus Scripts

This is a repository for scripts that I am writing as a part of my virus research SIP under Dr.Wilson at Kalamazoo
College

# find_aas.py

This script takes in virus capsid and point array PDB files and output creates/overwrtes an excel file called <virusname>.xlsx
with the closest Amino Acid in the capsid to each point in the PA for each chain, along with the distance and Atom at that point, and
the nearest other AA if there is one within 5 Angstroms.

To run (with capsid '2g33.pdb' and point array 'pa_346.pdb' in the same directory as the script):

```bash
python find_aas.py 2g33.pdb pa_346.pdb
```
