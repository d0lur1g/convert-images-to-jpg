from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from core.entities import ConversionResult

class IImageConverter(ABC):
    """Interface pour les convertisseurs d'images."""
    
    @abstractmethod
    def convert(self, input_path: Path, output_path: Path, quality: int) -> ConversionResult:
        """Convertit une image vers le format JPG."""
        pass
    
    @abstractmethod
    def supports_format(self, file_extension: str) -> bool:
        """Vérifie si le format est supporté."""
        pass
