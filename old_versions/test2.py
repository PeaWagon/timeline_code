import random

ProP_res = ['GLU', 'HIS', 'TYR', 'ASP', 'ASN', 'ILE', 'GLU', 'GLN', 'LYS', 'ILE', 'ASP', 'ASP', 'ILE', 'ASP', 'HIS', 'GLU', 'ILE', 'ALA', 'ASP', 'LEU', 'GLN', 'ALA', 'LYS', 'ARG', 'THR', 'ARG', 'LEU', 'VAL', 'GLN', 'GLN', 'HIS', 'PRO', 'ARG', 'ILE', 'ASP', 'GLU']
    
residue = random.choice(ProP_res)
print(residue)

res_desc = { 'non-polar, aliphatic': ['GLY', 'ALA', 'LEU', 'ILE', 'PRO'], 'aromatic': ['PHE', 'TYR', 'TRP'], 'polar, non-charged': ['SER', 'THR', 'CYS', 'MET', 'ASN', 'GLN'], 'positively charged': ['LYS', 'ARG', 'HIS'], 'negatively charged': ['ASP', 'GLU'] }

for key in res_desc:
    if residue in res_desc[key]:
        print(key)
