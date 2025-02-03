from .luminance import ImageLuminance

NODE_CLASS_MAPPINGS = {
    "ImageLuminance": ImageLuminance
}

NODE_DISPLAY_NAMES_MAPPINGS = {
    "ImageLuminance": "Image Luminance"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']