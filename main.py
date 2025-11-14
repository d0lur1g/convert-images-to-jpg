#!/usr/bin/env python3
"""
Convertisseur d'images universel vers JPG
Supporte : HEIC, PNG, JPEG, BMP, TIFF, WebP, GIF
"""

import sys
import logging
from pathlib import Path
from infrastructure.cli import parse_arguments, setup_logging
from core.use_cases import ConversionService
from adapters.converters import UniversalImageConverter, HEICConverter

def print_summary(results):
    """Affiche un résumé de la conversion."""
    success_count = len(results['success'])
    failed_count = len(results['failed'])
    total = success_count + failed_count
    
    print("\n" + "="*60)
    print("📊 RAPPORT DE CONVERSION")
    print("="*60)
    print(f"✓ Réussies : {success_count}/{total}")
    print(f"✗ Échouées : {failed_count}/{total}")
    
    if results['success']:
        total_before = sum(r.file_size_before or 0 for r in results['success'])
        total_after = sum(r.file_size_after or 0 for r in results['success'])
        
        # ✅ CORRECTION : Calcul clair de la différence
        size_diff = total_after - total_before
        percent_change = (size_diff / total_before) * 100 if total_before > 0 else 0
        
        # ✅ NOUVEAU : Affichage lisible
        print(f"\n💾 Taille totale avant : {total_before / (1024**2):.2f} MB")
        print(f"💾 Taille totale après : {total_after / (1024**2):.2f} MB")
        print(f"📊 Différence : {size_diff / (1024**2):+.2f} MB")  # +127 MB ou -50 MB
        
        # Affichage clair selon augmentation/réduction
        if percent_change > 0:
            print(f"⚠️  Augmentation : +{percent_change:.1f}% ({int(size_diff / (1024**2))} MB de plus)")
        elif percent_change < 0:
            print(f"✅ Réduction : {percent_change:.1f}% ({int(-size_diff / (1024**2))} MB de moins)")
        else:
            print(f"➡️  Taille stable")
    
    if results['failed']:
        print(f"\n⚠️  Fichiers en erreur :")
        for result in results['failed'][:5]:
            print(f"  - {result.source_path.name}: {result.error_message}")
        
        if failed_count > 5:
            print(f"  ... et {failed_count - 5} autre(s)")
    
    print("="*60 + "\n")

def main():
    """Point d'entrée principal."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Validation des chemins
    if not args.input.exists():
        logger.error(f"❌ Le dossier d'entrée n'existe pas : {args.input}")
        sys.exit(1)
    
    if not args.input.is_dir():
        logger.error(f"❌ Le chemin d'entrée n'est pas un dossier : {args.input}")
        sys.exit(1)
    
    # Initialisation du service
    converters = [
        HEICConverter(),
        UniversalImageConverter()
    ]
    
    service = ConversionService(converters=converters, quality=args.quality)
    
    # Conversion
    logger.info(f"🚀 Démarrage de la conversion (qualité: {args.quality})")
    logger.info(f"📂 Entrée  : {args.input.absolute()}")
    logger.info(f"📂 Sortie  : {args.output.absolute()}")
    logger.info(f"🔄 Récursif : {'Oui' if args.recursive else 'Non'}")
    
    try:
        results = service.convert_directory(
            input_dir=args.input,
            output_dir=args.output,
            recursive=args.recursive
        )
        
        print_summary(results)
        
        if results['failed']:
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Interruption utilisateur")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"❌ Erreur fatale : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
