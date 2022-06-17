import scipy
import scipy.spatial as spatial
import numpy as np
import pandas as pd
import sys

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
        aa_distances = scipy.spatial.distance.cdist(np.array(pa_coords[i]).reshape((1, 3)), pdb_full)
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
from openpyxl.styles import Alignment

xl_file = pdb_url.split('/')[-1].split('.')[0] + '.xlsx'
pa_name=pa_url.split('/')[-1].split('.')[0]
try:
    with pd.ExcelWriter(xl_file, engine="openpyxl", mode='a', if_sheet_exists='replace') as writer:
        point_df.to_excel(writer, startrow=1, sheet_name=pa_name, index = False)
except Exception as e: 
    point_df.to_excel(xl_file, sheet_name=pa_name, startrow = 1, index = False)
    print(e)

def excel_style(col):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    """ Convert given row and column number to an Excel-style cell name. """
    result = []
    while col:
        col, rem = divmod(col-1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result)

for df in dfs:
    with pd.ExcelWriter(xl_file, engine="openpyxl", mode='a', if_sheet_exists='overlay') as writer:  
        book = load_workbook(xl_file)
        writer.sheets = {ws.title: ws for ws in book.worksheets}
        writer.book = book
        for sheetname in writer.sheets:
            if sheetname != pa_name: continue
            scol = writer.sheets[sheetname].max_column
            mstring = excel_style(scol+1) + '1' + ':' + excel_style(scol+4) + '1'
            writer.sheets[sheetname].merge_cells(mstring)
            cstring = excel_style(scol+1).upper() + '1'
            writer.sheets[sheetname][cstring].alignment = Alignment(horizontal='center')
            writer.sheets[sheetname][cstring] = 'Chain ' + excel_style(scol // 4 + 1).upper()
            df.to_excel(writer, startrow = 1, sheet_name=sheetname, startcol=scol, index = False)
