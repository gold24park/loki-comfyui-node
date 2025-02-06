import numpy as np
import base64
from io import BytesIO
from PIL import Image
import torch
import cv2
import base64

class Base64ToImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base64_string": ("STRING", {"default": ""})
            }
        }
    RETURN_TYPES = ("IMAGE","MASK")
    RETURN_NAMES = ("image","mask")
    FUNCTION = "decode_base64"
    CATEGORY = "LokiComfyUINode/Image Processing"
    
    def convert_color(self, image):
        if len(image.shape) > 2 and image.shape[2] >= 4:
            return cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def decode_base64(self, base64_string):
        nparr = np.frombuffer(base64.b64decode(base64_string), np.uint8)

        result = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        channels = cv2.split(result)
        print(f"================channels_size: {len(channels)}")
        if len(channels) > 3:
            mask = channels[3].astype(np.float32) / 255.0
            mask = torch.from_numpy(mask)
        else:
            mask = torch.ones(channels[0].shape, dtype=torch.float32, device="cpu")

        result = self.convert_color(result)
        result = result.astype(np.float32) / 255.0
        image = torch.from_numpy(result)[None,]
        return image, mask.unsqueeze(0)
    
