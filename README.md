# 📸 Convert Images to JPG

Convertisseur d'images universel vers JPG avec support des formats HEIC (iPhone), PNG, JPEG, BMP, TIFF, WebP et GIF. Préserve automatiquement les profils de couleur (ICC) pour une fidélité maximale.

---

## 🎯 Fonctionnalités principales

- **Conversion multi-formats** : HEIC, PNG, JPEG, BMP, TIFF, WebP, GIF → JPG
- **Préservation des couleurs** : Extraction et conservation du profil ICC (sRGB, Display P3, etc.)
- **Qualité configurable** : De 1 à 100 (recommandé : 85)
- **Compression optimisée** : Mode progressif JPEG + choix du sous-échantillonnage
- **Traitement récursif** : Option pour parcourir les sous-dossiers
- **Rapport détaillé** : Statistiques de conversion (taille avant/après, succès/erreurs)
- **Logs structurés** : Traçabilité complète avec mode DEBUG optionnel

---

## 📋 Prérequis

- **Python 3.8+**
- **Pillow 10.0+** : Manipulation d'images
- **pillow-heif 0.13+** : Support du format HEIC (iPhone)

### Installation des dépendances système (selon OS)

#### Windows
```bash
# Installer via pip (recommandé)
pip install Pillow pillow-heif
```

#### Linux (Debian/Ubuntu)
```bash
sudo apt install libheif-dev
pip install Pillow pillow-heif
```

#### macOS
```bash
brew install libheif
pip install Pillow pillow-heif
```

---

## 🚀 Installation

### 1. Cloner ou télécharger le projet
```bash
git clone <repo-url>
cd convert-images-to-jpg
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
```

### 3. Activer l'environnement

**Windows (PowerShell)** :
```bash
venv\Scripts\Activate.ps1
```

**Windows (CMD)** :
```bash
venv\Scripts\activate.bat
```

**Linux/macOS** :
```bash
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

**Fichier `requirements.txt`** :
```
Pillow>=10.0.0
pillow-heif>=0.13.0
```

---

## 📂 Structure du projet

```
convert-images-to-jpg/
├── core/
│   ├── __init__.py
│   ├── entities.py           # Modèles de données (ConversionResult)
│   ├── interfaces.py         # Contrats (IImageConverter)
│   └── use_cases.py          # Logique métier (ConversionService)
├── adapters/
│   ├── __init__.py
│   └── converters.py         # Implémentations (UniversalImageConverter, HEICConverter)
├── infrastructure/
│   ├── __init__.py
│   └── cli.py                # Interface CLI (argparse)
├── main.py                   # Point d'entrée
├── requirements.txt
└── README.md
```

---

## 💻 Utilisation

### Syntaxe générale
```bash
python main.py -i <dossier_source> -o <dossier_destination> [options]
```

### Exemples d'utilisation

#### 1. Conversion simple (qualité 95)
```bash
python main.py -i "D:\Photos\iPhone" -o "D:\Photos\Converted"
```

#### 2. Qualité optimisée (85 = excellent rapport qualité/taille)
```bash
python main.py -i "D:\Photos\iPhone" -o "D:\Photos\Converted" -q 85
```

#### 3. Avec traitement récursif des sous-dossiers
```bash
python main.py -i "D:\Photos" -o "D:\Photos\Converted" -r -q 85
```

#### 4. Mode verbose (affiche les détails en DEBUG)
```bash
python main.py -i "D:\Photos\iPhone" -o "D:\Photos\Converted" -q 85 -v
```

#### 5. Tous les paramètres
```bash
python main.py -i "D:\Photos\iPhone" -o "D:\Photos\Converted" -q 85 -r -v
```

---

## 🎛️ Options disponibles

| Option | Court | Type | Défaut | Description |
|--------|-------|------|--------|-------------|
| `--input` | `-i` | `Path` | ✅ Obligatoire | Dossier source contenant les images |
| `--output` | `-o` | `Path` | ✅ Obligatoire | Dossier destination pour les JPG |
| `--quality` | `-q` | `int` [1-100] | `95` | Qualité de compression JPG |
| `--recursive` | `-r` | `flag` | `False` | Traiter récursivement les sous-dossiers |
| `--verbose` | `-v` | `flag` | `False` | Afficher les logs DEBUG |
| `--help` | `-h` | `flag` | — | Afficher l'aide |

### Recommandations de qualité

| Qualité | Cas d'usage | Taille vs original |
|---------|------------|-------------------|
| **95-100** | Archives, impression haute résolution | 120-150% |
| **85-90** | Usage général, web, affichage (⭐ RECOMMANDÉ) | 100-120% |
| **75-80** | Compression modérée, économie d'espace | 80-100% |
| **60-70** | Compression forte, partage web | 50-80% |

---

## 📊 Exemple de résultat

```
🚀 Démarrage de la conversion (qualité: 85)
📂 Entrée  : D:\A traiter\01_iPhone\VRACS - A TRIER
📂 Sortie  : D:\A traiter\01_iPhone\VRACS - A TRIER\convert-images-to-jpg
🔄 Récursif : Non

2025-11-14 23:45:12 - INFO - Traitement de 150 fichiers depuis D:\A traiter\01_iPhone\VRACS - A TRIER
2025-11-14 23:45:13 - INFO - ✓ photo_001.HEIC → photo_001.jpg (2048KB → 1850KB)
2025-11-14 23:45:13 - INFO - ✓ photo_002.HEIC → photo_002.jpg (1920KB → 1760KB)
...

============================================================
📊 RAPPORT DE CONVERSION
============================================================
✓ Réussies : 148/150
✗ Échouées : 2/150

💾 Taille totale avant : 847.01 MB
💾 Taille totale après : 975.00 MB
📊 Différence : +127.99 MB
⚠️  Augmentation : +15.1% (128 MB de plus)

⚠️  Fichiers en erreur :
  - corrupted_img.HEIC: invalid HEIF file
  - unsupported.bmp: Format non supporté : .bmp
============================================================
```

---

## 🔍 Formats supportés

### Formats d'entrée

| Format | Extension | Notes |
|--------|-----------|-------|
| **HEIC** | `.heic`, `.heif` | Format Apple (iPhone) - profil ICC préservé |
| **JPEG** | `.jpeg`, `.jpg` | Profil ICC préservé si présent |
| **PNG** | `.png` | Conversion RGB, transparence → blanc |
| **BMP** | `.bmp` | Format bitmap standard |
| **TIFF** | `.tiff`, `.tif` | Format d'archive sans perte |
| **WebP** | `.webp` | Format moderne web |
| **GIF** | `.gif` | Images animées (conversion premier frame) |

### Format de sortie

- **JPEG** (`.jpg`) : Compression avec profil ICC préservé, mode progressif activé

---

## 🎨 Gestion des couleurs

### Profils ICC (International Color Consortium)

Le convertisseur préserve automatiquement les profils de couleur :

- ✅ **HEIC** : Profil ICC extrait et appliqué au JPG
- ✅ **PNG/JPEG** : Profil ICC préservé si disponible
- ✅ **Autres formats** : Conversion en sRGB standard

### Modes de couleur gérés

| Mode | Traitement |
|------|-----------|
| RGB | Direct (aucune conversion) |
| RGBA | Conversion RGB + fond blanc |
| LA (Grayscale + Alpha) | Conversion RGB + fond blanc |
| Palette (P) | Conversion RGB directe |
| CMYK | Conversion RGB (format imprimerie) |

### Paramètres JPEG optimisés

- **Qualité** : Configurable (recommandé 85)
- **Optimisation** : Activée (compression supplémentaire sans perte visuelle)
- **Mode progressif** : Activé (chargement progressif sur web)
- **Sous-échantillonnage** : 4:4:4 (HEIC) ou 4:2:0 (Universal) - préserve la chrominance

---

## ⚙️ Architecture technique

### Design Pattern : Clean Architecture

```
┌─────────────────────────────────────┐
│     Infrastructure (CLI, I/O)       │
│        main.py, cli.py              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    Adapters (Implémentations)       │
│  UniversalImageConverter            │
│  HEICConverter                      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│     Core (Domaine métier)           │
│  ConversionService                  │
│  Interfaces & Entities              │
└─────────────────────────────────────┘
```

### Principes SOLID appliqués

- **S**ingle Responsibility : Chaque classe a une responsabilité unique
- **O**pen/Closed : Extensible sans modifier le code existant
- **I**nterface Segregation : Interfaces minimales et focalisées
- **D**ependency Inversion : Dépendances sur les abstractions

---

## 🛠️ Dépannage

### Problème : "Le dossier d'entrée n'existe pas"

**Cause** : Le chemin est incorrect ou inaccessible

**Solutions** :
```bash
# Vérifier que le chemin existe
dir "D:\A traiter\01_iPhone"

# Utiliser des slashs simples (Windows accepte les deux)
python main.py -i "D:/A traiter/01_iPhone" -o "D:/output"

# Vérifier les permissions de lecture
# Windows : Clic droit → Propriétés → Sécurité
```

---

### Problème : "Erreur lors de la conversion : object of type 'NoneType' has no len()"

**Cause** : Image corrompue ou format non géré correctement

**Solution** :
```bash
# Lancer en mode verbose pour identifier le fichier
python main.py -i "D:\A traiter\01_iPhone" -o "D:\output" -v

# Le fichier problématique sera affichage dans les logs
# Supprimer le fichier et relancer la conversion
```

---

### Problème : "ImportError: cannot import name 'IImageConverter'"

**Cause** : Fichiers manquants ou structure du projet incorrecte

**Solution** :
```bash
# Vérifier la présence de tous les fichiers __init__.py
ls core/__init__.py
ls adapters/__init__.py
ls infrastructure/__init__.py

# Nettoyer les fichiers .pyc
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
```

---

### Problème : "FileNotFoundError: [Errno 2] No such file or directory: 'pillow-heif'"

**Cause** : pillow-heif non installée

**Solution** :
```bash
# Installer explicitement
pip install pillow-heif --upgrade

# Sur Linux, installer aussi la dépendance système
sudo apt install libheif-dev
pip install pillow-heif
```

---

### Problème : Les couleurs ne correspondent pas à l'original

**Cause** : Profil ICC non appliqué ou codage différent

**Solutions** :
```bash
# Mode verbose pour voir si le profil ICC est appliqué
python main.py -i "..." -o "..." -v

# Les logs affichent "Profil ICC appliqué" si succès
# Sinon, c'est une limitation du fichier source
```

---

## 📈 Optimisation et performances

### Pour améliorer la vitesse

1. **Réduire la qualité** : `-q 75` au lieu de `-q 85`
2. **Réduire les dimensions** : Option future (scale parameter)
3. **Traitement parallèle** : Option future (multithreading)

### Pour améliorer la qualité

1. **Augmenter la qualité** : `-q 90` ou `-q 95`
2. **Vérifier le profil ICC** : Actif automatiquement
3. **Vérifier l'image source** : HEIC avec profil Display P3

### Estimations de taille

| Situation | Avant | Après (-q85) | Gain |
|-----------|-------|--------------|------|
| HEIC 12MP | 2 MB | 2.3 MB | -15% (augmentation) |
| JPEG 12MP | 3 MB | 3.2 MB | -5% |
| PNG 12MP | 8 MB | 2.5 MB | +70% |

---

## 📝 Logs et débogage

### Activer les logs DEBUG

```bash
python main.py -i "..." -o "..." -v
```

### Interpréter les logs

```
INFO - Traitement de 150 fichiers     # Phase d'initialisation
INFO - ✓ photo.HEIC → photo.jpg       # Conversion réussie
ERROR - ✗ Échec conversion photo.jpg  # Conversion échouée + raison
```

### Fichier de logs (optionnel)

Pour sauvegarder les logs dans un fichier, modifier `infrastructure/cli.py` :

```python
logging.basicConfig(
    level=level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),  # Affichage console
        logging.FileHandler('conversion.log')  # Fichier
    ]
)
```

---

## 🚀 Évolutions futures

- [ ] **Paramètre `--scale`** : Réduire les dimensions des images
- [ ] **Paramètre `--delete-source`** : Supprimer les fichiers source après conversion
- [ ] **Traitement parallèle** : Utiliser ThreadPoolExecutor pour +300% de vitesse
- [ ] **Interface graphique** : PyQt6 ou Tkinter
- [ ] **Mode watch** : Conversion automatique à l'ajout de fichiers
- [ ] **Compression intelligente** : Ajustement qualité selon taille source
- [ ] **Support RAW** : CR2, NEF, ARW via rawpy
- [ ] **Batch processing** : Traiter les images par lots

---

## 📜 Licence

MIT - Libre d'utilisation et de modification

---

## 💬 Support & Contributions

Pour signaler un bug ou proposer une amélioration :

1. Vérifier qu'il n'existe pas déjà
2. Créer un issue détaillé avec :
   - Version Python (`python --version`)
   - Système d'exploitation (Windows/Linux/macOS)
   - Commande utilisée et message d'erreur complet
   - Logs en mode verbose (`-v`)

---

## 🔧 Détails techniques

### Dépendances principales

- **Pillow 10.0+** : PIL/Pillow pour manipulation d'images
  - Compression JPEG
  - Gestion des profils ICC
  - Support du mode progressif
  
- **pillow-heif 0.13+** : Plugin HEIF pour Pillow
  - Décodage HEIC/HEIF
  - Extraction du profil ICC

### Versions compatibles

| Python | Status |
|--------|--------|
| 3.8 | ✅ Supporté |
| 3.9 | ✅ Supporté |
| 3.10 | ✅ Supporté |
| 3.11 | ✅ Supporté |
| 3.12 | ✅ Supporté |

---

## 📞 Auteur

Développé par **Ludo** - 2025

Basé sur Clean Architecture et SOLID principles.

---

**Besoin d'aide ?** Consulte la section [Dépannage](#-dépannage) ou lance `python main.py -h` pour l'aide intégrée.
