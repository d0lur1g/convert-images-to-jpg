import argparse
import logging
from pathlib import Path

def setup_logging(verbose: bool):
    """Configure le système de logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_arguments():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Convertisseur d'images vers JPG (HEIC, PNG, JPEG, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py -i ./photos -o ./output
  python main.py -i /data/images -o /data/jpg -r -q 90 -v
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=Path,
        required=True,
        help='Dossier contenant les images à convertir'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        required=True,
        help='Dossier de destination pour les fichiers JPG'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Traiter récursivement les sous-dossiers'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=95,
        choices=range(1, 101),
        metavar='[1-100]',
        help='Qualité de compression JPG (défaut: 95)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Afficher les logs détaillés (DEBUG)'
    )
    
    return parser.parse_args()
