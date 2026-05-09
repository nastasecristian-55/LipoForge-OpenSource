import sys
import os
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
from rdkit import RDConfig
import py3Dmol
import tempfile

def calculate_lipinski(name, smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if not mol: return f"Error: Invalid SMILES for {name}", False
        
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hba = Descriptors.NumHAcceptors(mol)
        hbd = Descriptors.NumHDonors(mol)
        tpsa = Descriptors.TPSA(mol)
        
        status = "FAIL ❌"
        if mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10 and tpsa <= 140:
            status = "PASS ✅"
            
        report = (f"{name}\n"
                  f"  MW: {mw:.0f} | LogP: {logp:.1f} | "
                  f"HBA: {hba} | HBD: {hbd} | TPSA: {tpsa:.0f} -> {status}\n"
                  f"{'-'*40}\n")
        return report, True
    except Exception as e:
        return f"Error analyzing {name}: {str(e)}\n", False

def generate_3d_html(library_dict):
    view = py3Dmol.view(width=1400, height=800)
    view.removeAllModels()

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        fdefName = os.path.join(base_path, 'rdkit', 'Data', 'BaseFeatures.fdef')
    else:
        fdefName = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')

    try:
        factory = AllChem.BuildFeatureFactory(fdefName)
    except Exception as e:
        return f"Error loading features: {e}"

    x_offset = 0
    
    for name, smiles in library_dict.items():
        mol = Chem.MolFromSmiles(smiles)
        if not mol: continue
        mol_3d = Chem.AddHs(mol)
        res = AllChem.EmbedMolecule(mol_3d, AllChem.ETKDG())
        if res == -1:
            res = AllChem.EmbedMolecule(mol_3d, AllChem.ETKDG(useRandomCoords=True))
        if res == -1:
            print(f"Failed to generate 3D for {name}")
            continue
            
        try: AllChem.MMFFOptimizeMolecule(mol_3d)
        except: pass 
        
        conf = mol_3d.GetConformer()
        for i in range(mol_3d.GetNumAtoms()):
            pos = conf.GetAtomPosition(i)
            conf.SetAtomPosition(i, (pos.x + x_offset, pos.y, pos.z))
            
        block = Chem.MolToMolBlock(mol_3d)
        view.addModel(block, 'mol_3d')
        
        feats = factory.GetFeaturesForMol(mol_3d)
        view.setStyle({'model': -1}, {'stick': {'colorscheme': 'grayCarbon', 'radius': 0.15}})
        
        for f in feats:
            pos = f.GetPos()
            if f.GetFamily() == 'Aromatic':
                view.addSphere({'center': {'x': pos.x, 'y': pos.y, 'z': pos.z}, 'radius': 1.5, 'color': 'blue', 'opacity': 0.3})
            elif f.GetFamily() == 'Donor':
                view.addSphere({'center': {'x': pos.x, 'y': pos.y, 'z': pos.z}, 'radius': 0.5, 'color': 'magenta', 'opacity': 0.8})
            elif f.GetFamily() == 'Acceptor':
                view.addSphere({'center': {'x': pos.x, 'y': pos.y, 'z': pos.z}, 'radius': 0.5, 'color': 'cyan', 'opacity': 0.8})
        
        view.addLabel(name, {'position': {'x': x_offset, 'y': 10, 'z': 0}, 'backgroundColor': 'black', 'fontColor': 'white'})
        
        x_offset += 25
    
    view.zoomTo()
    html_content = view._make_html()
    temp_dir = tempfile.gettempdir()
    output_file = os.path.join(temp_dir, "molecular_viewer.html")
    with open(output_file, "w") as f:
        f.write(html_content)   
    return output_file
