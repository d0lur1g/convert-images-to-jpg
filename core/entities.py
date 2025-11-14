from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class ConversionResult:
    """Résultat d'une conversion d'image."""
    source_path: Path
    destination_path: Optional[Path]
    success: bool
    error_message: Optional[str] = None
    file_size_before: Optional[int] = None
    file_size_after: Optional[int] = None
