![Status](https://img.shields.io/badge/Status-Stable-green)
![Field](https://img.shields.io/badge/Field-Computational%20Chemistry-blue)
![Education](https://img.shields.io/badge/Purpose-Educational-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey)

# LipoForge v1.0.0
**Lightweight Cheminformatics for the Modern Lab.** *Developed by Cristian Năstase*

<br>

**What is it?**
LipoForge is a tool I built to bridge the gap between flat 2D chemical strings and 3D molecular reality. It targets students and researchers who need a quick, no-fuss way to validate drug-likeness and visualize pharmacophores without opening heavy, expensive software.

**Core Specs:**
* **Lipinski & Veber Screening:** Fast calculation of MW, LogP, HBA, HBD, and TPSA.
* **Interactive 3D:** Real-time generation of molecular conformers.
* **Smart Mapping:** Visual cues for Aromatic Rings (Blue), H-Donors (Magenta), and H-Acceptors (Cyan).
* **Stability:** Custom RDKit embedding logic to prevent conformer crashes.

<br>

**Getting Started**

**1. Standalone Apps (Easiest)**
Grab the pre-built binaries from the **[Releases](../../releases)** tab.
* **Windows:** Unzip and run `LipoForge.exe`.
* **macOS:** Drag `LipoForge.app` to your Applications folder.

**2. Developer Setup (Run from Source)**
```bash
# Clone the repo
git clone [https://github.com/nastasecristian-55/LipoForge-OpenSource.git](https://github.com/nastasecristian-55/LipoForge-OpenSource.git)
cd SyndicateLabs

# Install dependencies
pip install -r requirements.txt

# Launch
python app_main.py
```

**Tech Stack**

GUI: CustomTkinter (Dark Mode)   
Brain: RDKit & Py3Dmol   
Environment: Developed on macOS for cross-platform utility.


**License & Credits**

License: MIT - Use it, fork it, learn from it.  
Context: Originally created as a final project for Didactica Domeniului at the University of Bucharest.  


Profesorul trăznit - over and out!
