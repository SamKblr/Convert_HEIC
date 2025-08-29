# Convertisseur HEIC → PNG avec interface graphique [Samuel, Kubler]

## 📖 Description

Ce projet permet de **convertir automatiquement tous les fichiers `.HEIC`** trouvés dans un répertoire source (et ses sous-dossiers) vers le format **`.png`**.  
Il a été développé pour faciliter la lecture des photos **iPhone** sur un PC **Windows**, sans avoir besoin d’installer de codec externe.  

Une **interface graphique (GUI)** a été créée afin de simplifier l’utilisation du programme pour les utilisateurs non techniques.  

---

## ✨ Fonctionnalités

- Parcours récursif d’un dossier source (et de ses sous-dossiers).  
- Conversion des fichiers **`.HEIC` → `.png`**.  
- Conservation de l’arborescence des dossiers dans le répertoire de sortie.  
- Interface graphique intuitive.  
- Possibilité de générer un **exécutable Windows (.exe)** pour utilisation sans Python.  

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/<TON_COMPTE_GITHUB>/<NOM_DU_REPO>.git
cd <NOM_DU_REPO>
```

###  2. Créer l'environnement virtuel

```bash
conda env create -f environment.yml
conda activate convert-heic
```
## Utilisation

### 1. Utilisation par code python

```bash
python src/gui.py
```
L’interface graphique s’ouvre, vous pouvez sélectionner le dossier source contenant vos fichiers HEIC et lancer la conversion.

### 2. Utilisation par exécutable

```bash
pyinstaller gui.spec
```

👉 L’exécutable sera disponible dans le dossier /dist/ sous le nom gui.exe.
Vous pouvez ensuite le lancer sans avoir besoin d’installer Python ou les dépendances.

## 📂 Structure du projet

```bash
.
├── src/               # Code source (fonctions + interface graphique)
│   ├── functions.py
│   ├── gui.py
│   └── __init__.py
│
├── notebooks/         # Notebook Jupyter pour tests et prototypage
│   └── convert_HEIC.ipynb
│
├── data/              # Dossier contenant les images d'entrée (.HEIC)
│   └── README.md
│
├── results/           # Résultats générés (.png)
│   └── README.md
│
├── environment.yml    # Dépendances conda
├── gui.spec           # Configuration PyInstaller
├── README.md          # Documentation du projet
└── .gitignore
```