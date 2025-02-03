from .luminance import ImageLuminance
from .dominant_color import DominantColor

NODE_CLASS_MAPPINGS = {
    "ImageLuminance": ImageLuminance,
    "DominantColor": DominantColor
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "ImageLuminance": "Get Image Luminance",
    "DominantColor": "Get Dominant Color"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']