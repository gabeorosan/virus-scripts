import scipy
import scipy.spatial as spatial
import numpy as np
import pandas as pd
import sys

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

pdb_url = sys.argv[1]
pa_url = sys.argv[2]

# read pdb file
with open(pdb_url) as pdb_file:
    pdb_lines = pdb_file.readlines()
    pdb_coords = {}
    pdb_full = np.zeros((len(pdb_lines), 3))
    pdb_aas = []
    for i in range(len(pdb_lines)):
        l = pdb_lines[i]
        chain = l[21]
        x = float(l[31:38])
        y = float(l[39:46])
        z = float(l[47:54])
        if chain not in pdb_coords.keys():
            pdb_coords[chain] = []
        pdb_coords[chain].append([x, y, z])
        pdb_full[i] = np.array([x, y, z])
        pdb_aas.append(l[17:20])

#read pa file
with open(pa_url) as pa_file:
    pa_coords = []
    for l in pa_file.readlines():
        x = float(l[31:38])
        y = float(l[39:46])
        z = float(l[47:54])
        pa_coords.append([x, y, z])

aa_distances = scipy.spatial.distance.cdist(np.array([-1.381, 50.242, 165.299]).reshape((1, 3)), pdb_full)

dfs = []
point_df = pd.DataFrame({'Point': range(1, len(pa_coords)+1)})
for c in pdb_coords.keys():
    distances = scipy.spatial.distance.cdist(pdb_coords[c], pa_coords)
    min_ixs = np.argmin(distances, axis=0)
    ds, atoms, aas, aa_others = [], [], [], []
    for i in range(len(min_ixs)):
        ix = min_ixs[i]
        d = distances[ix][i]
        aa = pdb_aas[ix]
        aa_rn = pdb_lines[ix][23:26]
        atom = pdb_lines[ix][13:16]
        aa_distances = scipy.spatial.distance.cdist(np.array(pdb_coords[c][ix]).reshape((1, 3)), pdb_full)
        d_argsort = np.argsort(aa_distances[0])
        for j in range(len(d_argsort)):
            c_ix = np.where(d_argsort==j)[0][0]
            if aa_distances[0][c_ix] > 5:
                aa_others.append('N/A')
                break
            elif pdb_aas[ix] + pdb_lines[ix][23:26] != pdb_aas[c_ix] + pdb_lines[c_ix][23:26]:
                aa_other_rn = pdb_aas[c_ix] + pdb_lines[c_ix][23:26]
                aa_others.append(aa_other_rn)
                break
        ds.append(d)
        atoms.append(atom)
        aas.append(aa + aa_rn)
        
    df = pd.DataFrame({'Distance': ds, 'Atom': atoms, 'AA/RN': aas, 'Other AA': aa_others})
    dfs.append(df)

from openpyxl import load_workbook

point_df.to_excel('test.xlsx', startrow = 1, index = False)

for df in dfs:
    with pd.ExcelWriter('test.xlsx', engine="openpyxl", mode='a', if_sheet_exists='overlay') as writer:  
        book = load_workbook('test.xlsx')
        writer.sheets = {ws.title: ws for ws in book.worksheets}
        for sheetname in writer.sheets:
            writer.book = book
            scol = writer.sheets[sheetname].max_column
            adict = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h', 9:'i', 10:'j', 11:'k', 12:'l', 13:'m', 14:'n', 15:'o', 16:'p', 17:'q', 18:'r', 19:'s', 20:'t', 21:'u', 22:'v', 23:'w', 24:'x', 25:'y', 26:'z'} 
            mstring = adict[scol+1].upper() + '1' + ':' + adict[scol+4].upper() + '1'
            writer.sheets[sheetname].merge_cells(mstring)
            cstring = adict[scol+1].upper() + '1'
            writer.sheets[sheetname][cstring] = 'Chain ' + adict[scol // 4 + 1].upper()
            df.to_excel(writer, startrow = 1, sheet_name=sheetname, startcol=scol, index = False)
