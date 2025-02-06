import base64
from io import BytesIO
from .functions_graphics import tensor2pil_rgba


class ImageToBase64:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"image": ("IMAGE",)}
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("base64",)
    FUNCTION = "encode_image"
    CATEGORY = "LokiComfyUINode/Image Processing"

    def encode_image(self, image):
        image = tensor2pil_rgba(image)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return (img_str,)
