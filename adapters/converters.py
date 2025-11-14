import logging
from pathlib import Path
from PIL import Image
import pillow_heif

from core.entities import ConversionResult
from core.interfaces import IImageConverter

class UniversalImageConverter(IImageConverter):
    """Convertisseur universel - formats standards (PNG, BMP, TIFF, etc.)."""
    
    SUPPORTED_FORMATS = {'.png', '.jpeg', '.jpg', '.bmp', '.tiff', '.tif', '.webp', '.gif'}
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def supports_format(self, file_extension: str) -> bool:
        return file_extension.lower() in self.SUPPORTED_FORMATS
    
    def convert(self, input_path: Path, output_path: Path, quality: int = 95) -> ConversionResult:
        try:
            size_before = input_path.stat().st_size
            
            with Image.open(input_path) as img:
                # ✅ Solution 1 : Extraire le profil ICC
                icc_profile = img.info.get('icc_profile', None)
                
                # Conversion des modes couleur
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    
                    if img.mode == 'RGBA' and len(img.split()) == 4:
                        alpha_channel = img.split()[3]
                        rgb_img.paste(img.convert('RGB'), mask=alpha_channel)
                    elif img.mode == 'LA' and len(img.split()) == 2:
                        alpha_channel = img.split()[1]
                        rgb_img.paste(img.convert('RGB'), mask=alpha_channel)
                    else:
                        rgb_img.paste(img.convert('RGB'))
                    
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # ✅ Solution 3 : Paramètres JPG optimisés pour la fidélité des couleurs
                save_kwargs = {
                    'format': 'JPEG',
                    'quality': quality,
                    'optimize': True,        
                    'progressive': True,      # ✅ Chargement progressif
                    'subsampling': 0          # ✅ Pas de sous-échantillonnage (4:4:4)
                }
                
                # ✅ Solution 1 : Sauvegarder AVEC le profil ICC
                if icc_profile:
                    save_kwargs['icc_profile'] = icc_profile
                
                img.save(output_path, **save_kwargs)
            
            size_after = output_path.stat().st_size
            self.logger.info(f"✓ {input_path.name} → {output_path.name} "
                           f"({size_before//1024}KB → {size_after//1024}KB)")
            
            return ConversionResult(
                source_path=input_path,
                destination_path=output_path,
                success=True,
                file_size_before=size_before,
                file_size_after=size_after
            )
            
        except Exception as e:
            self.logger.error(f"✗ Échec conversion {input_path.name}: {e}")
            return ConversionResult(
                source_path=input_path,
                destination_path=None,
                success=False,
                error_message=str(e)
            )


class HEICConverter(IImageConverter):
    """Convertisseur spécialisé pour le format HEIC (Apple)."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        pillow_heif.register_heif_opener()
    
    def supports_format(self, file_extension: str) -> bool:
        return file_extension.lower() in {'.heic', '.heif'}
    
    def convert(self, input_path: Path, output_path: Path, quality: int = 95) -> ConversionResult:
        try:
            size_before = input_path.stat().st_size
            
            # Chargement HEIC
            heif_file = pillow_heif.open_heif(input_path)
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data, 
                "raw"
            )
            
            # ✅ Solution 1 : Extraire le profil ICC du HEIC
            # Attention : accéder à heif_file.info selon la version de pillow_heif
            icc_profile = None
            try:
                icc_profile = heif_file.info.get('icc_profile', None)
            except:
                pass  # Version ancienne de pillow_heif
            
            # Conversion RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # ✅ Solution 3 : Paramètres JPG optimisés
            save_kwargs = {
                'format': 'JPEG',
                'quality': quality,
                'optimize': False,        # ✅ Préserver les couleurs
                'progressive': True,      # ✅ Chargement progressif
                'subsampling': 0          # ✅ Pas de compression chrominance
            }
            
            # ✅ Solution 1 : Appliquer le profil ICC
            if icc_profile:
                save_kwargs['icc_profile'] = icc_profile
            
            image.save(output_path, **save_kwargs)
            
            size_after = output_path.stat().st_size
            self.logger.info(f"✓ {input_path.name} → {output_path.name} "
                           f"({size_before//1024}KB → {size_after//1024}KB)")
            
            return ConversionResult(
                source_path=input_path,
                destination_path=output_path,
                success=True,
                file_size_before=size_before,
                file_size_after=size_after
            )
            
        except Exception as e:
            self.logger.error(f"✗ Échec conversion HEIC {input_path.name}: {e}")
            return ConversionResult(
                source_path=input_path,
                destination_path=None,
                success=False,
                error_message=str(e)
            )
