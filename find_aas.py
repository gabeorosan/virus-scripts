import sys

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

pdb_url = sys.argv[1]
pa_url = sys.argv[2]

if len(sys.argv) > 3:
    n_acids = int(sys.argv[3])
else: n_acids = 5

# read pdb file
with open(pdb_url) as pdb_file:
    pdb_lines = pdb_file.readlines()
    aas = [l.split()[3] for l in pdb_lines]
    pdb_coords = []
    for l in pdb_lines:
        x = float(l[31:38])
        y = float(l[39:46])
        z = float(l[47:54])
        pdb_coords.append([x, y, z])
    
#read pa file
with open(pa_url) as pa_file:
    pa_coords = []
    for l in pa_file.readlines():
        x = float(l[31:38])
        y = float(l[39:46])
        z = float(l[47:54])
        pa_coords.append([x, y, z])
#compute distances
distances = []
for i in range(len(pa_coords)):
    ds = []
    for j in range(len(pdb_coords)):
        ds.append(((pdb_coords[j][0] - pa_coords[i][0])**2 + (pdb_coords[j][1] - pa_coords[i][1])**2 + (pdb_coords[j][2] - pa_coords[i][2])**2)**.5)
    distances.append(ds)

#get info of closest atoms
pa_matrix = []
for i in range(len(pa_coords)):
    aa_info = []
    min_ixs = argsort(distances[i])
    for j in range(n_acids):
        ix = min_ixs[j]
        aa = pdb_lines[ix][18:20]
        atom = pdb_lines[ix][13:16]
        chain = pdb_lines[ix][21]
        distance = distances[i][ix]
        aa_info.append([aa, atom, distance, chain])
    pa_matrix.append(aa_info)
with open('aa_info.txt', 'w') as f:
    for i in range(len(pa_matrix)):
        f.write('\npoint: ' + str(i+1)+ '\n')
        for aa in pa_matrix[i]:
            f.write("\nAmino Acid: " + str(aa[0]))
            f.write("\nAtom: " + str(aa[1]))
            f.write("\nDistance: " + str(aa[2]))
            f.write("\nChain: " + str(aa[3]) + '\n')
print(pa_matrix)

