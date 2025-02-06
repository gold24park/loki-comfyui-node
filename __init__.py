from .saturation import ImageSaturation
from .image_to_base64 import ImageToBase64
from .base64_to_image import Base64ToImage
from .luminance import ImageLuminance
from .dominant_color import DominantColor
from .overlay_text import OverlayText

NODE_CLASS_MAPPINGS = {
    "ImageLuminance": ImageLuminance,
    "DominantColor": DominantColor,
    "OverlayText": OverlayText,
    "Base64ToImage": Base64ToImage,
    "ImageToBase64": ImageToBase64,
    "ImageSaturation": ImageSaturation
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "ImageLuminance": "Get Image Luminance",
    "DominantColor": "Get Dominant Color",
    "OverlayText": "Overlay Text",
    "Base64ToImage": "Base64 to Image",
    "ImageToBase64": "Image (PNG) to Base64",
    "Saturation": "Get Image Saturation"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']