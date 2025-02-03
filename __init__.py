from .luminance import ImageLuminance
from .dominant_color import DominantColor
from .overlay_text import OverlayText

NODE_CLASS_MAPPINGS = {
    "ImageLuminance": ImageLuminance,
    "DominantColor": DominantColor,
    "OverlayText": OverlayText
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "ImageLuminance": "Get Image Luminance",
    "DominantColor": "Get Dominant Color",
    "OverlayText": "Overlay Text"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']