import logging
from pathlib import Path
from typing import List, Dict
from core.entities import ConversionResult
from core.interfaces import IImageConverter

class ConversionService:
    """Service orchestrant la conversion d'images."""
    
    def __init__(self, converters: List[IImageConverter], quality: int = 95):
        self.converters = converters
        self.quality = quality
        self.logger = logging.getLogger(__name__)
    
    def convert_directory(
        self, 
        input_dir: Path, 
        output_dir: Path, 
        recursive: bool = False
    ) -> Dict[str, List[ConversionResult]]:
        """Convertit toutes les images d'un répertoire."""
        
        output_dir.mkdir(parents=True, exist_ok=True)
        results = {"success": [], "failed": []}
        
        # Collecte des fichiers
        pattern = "**/*" if recursive else "*"
        files = [f for f in input_dir.glob(pattern) if f.is_file()]
        
        self.logger.info(f"Traitement de {len(files)} fichiers depuis {input_dir}")
        
        for file_path in files:
            result = self._convert_single_file(file_path, output_dir)
            
            if result.success:
                results["success"].append(result)
            else:
                results["failed"].append(result)
        
        return results
    
    def _convert_single_file(self, input_path: Path, output_dir: Path) -> ConversionResult:
        """Convertit un fichier unique."""
        
        # Recherche du convertisseur approprié
        converter = self._find_converter(input_path.suffix.lower())
        
        if not converter:
            return ConversionResult(
                source_path=input_path,
                destination_path=None,
                success=False,
                error_message=f"Format non supporté : {input_path.suffix}"
            )
        
        # Construction du chemin de sortie
        output_path = output_dir / f"{input_path.stem}.jpg"
        
        # Conversion
        try:
            return converter.convert(input_path, output_path, self.quality)
        except Exception as e:
            self.logger.error(f"Erreur inattendue sur {input_path}: {e}")
            return ConversionResult(
                source_path=input_path,
                destination_path=None,
                success=False,
                error_message=str(e)
            )
    
    def _find_converter(self, extension: str) -> IImageConverter:
        """Trouve le convertisseur approprié pour une extension."""
        for converter in self.converters:
            if converter.supports_format(extension):
                return converter
        return None
