import sys, os

def parse_PDB(PDBfile):
    protein = []; ligand = []
    for line in PDBfile:
        line_1 = line.strip().split()
        if len(line_1):
            if line_1[0] == 'ATOM':
                protein.append(line)
            elif line_1[0] == 'HETATM':
                ligand.append(line)
    return protein, ligand
    
def get_center_coord(ligand):
    ligand_1 = list(ligand)
    for i in range(len(ligand_1)):
        ligand_1[i] = ligand_1[i].strip().split()
    ligand_trans = zip(*ligand_1)
    coord_x = sum(map(float, ligand_trans[6]))/float(len(ligand_trans[6]))
    coord_y = sum(map(float, ligand_trans[7]))/float(len(ligand_trans[7]))
    coord_z = sum(map(float, ligand_trans[8]))/float(len(ligand_trans[8]))
    center_coord = tuple([coord_x, coord_y, coord_z])
    return center_coord
    
def write_PDB(pdb, pdb_name):
    with open(pdb_name, 'wb') as f:
        for i in pdb:
            f.write(i)
    
def dock_vina(PDBfile, PDBname):
    protein, ligand = parse_PDB(PDBfile)
    center_coord = get_center_coord(ligand)
    protein_pdb = PDBname + '_protein.pdb'
    ligand_pdb = PDBname + '_ligand.pdb'
    write_PDB(protein, protein_pdb)
    write_PDB(ligand, ligand_pdb)
    protein_pdbqt = protein_pdb+'qt'
    ligand_pdbqt = ligand_pdb+'qt'
    cmd_protein = 'prepare_receptor4.py -r %s -o %s -v'%(protein_pdb, protein_pdbqt)
    cmd_ligand = 'prepare_ligand4.py -l %s -o %s -v'%(ligand_pdb, ligand_pdbqt)
    os.system(cmd_protein)
    os.system(cmd_ligand)
    cmd_vina = 'vina --receptor %s --ligand %s --center_x %s --center_y %s --center_z %s \
                --size_x 10 --size_y 10 --size_z 10 --out %s --log %s --cpu 1 --num_modes 1' \
                %(protein_pdbqt, ligand_pdbqt, center_coord[0], center_coord[1], center_coord[2], \
                  PDBname+'_dock_pose.pdb', PDBname+'_dock_log')
    docking = os.popen(cmd_vina)
    #print docking.read()
    
if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        for line in f:
            pdb_name = line.strip()
            print '-------------------\n',pdb_name
            PDBfile = open(pdb_name, 'rb')
            PDBname = pdb_name.split('.')[0]
            dock_vina(PDBfile, PDBname)