import torch
import numpy as np

class ImageLuminance:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "image": ("IMAGE",)
            }
        }
        return inputs
    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("luminance",)
    FUNCTION = "get_luminance"
    OUTPUT_NODE = True
    CATEGORY = "LokiComfyUINode/Image Analysis"
    
    def get_luminance(self, image):
        # ComfyUI의 이미지 텐서를 numpy 배열로 변환
        if isinstance(image, torch.Tensor):
            # (batch, height, width, channels) -> (height, width, channels)``
            if len(image.shape) == 4:
                image = image[0]
            image_np = image.cpu().numpy()
        else:
            image_np = np.array(image)
        
        # RGB to Luminance 변환 (Y = 0.2126R + 0.7152G + 0.0722B)
        if image_np.shape[-1] >= 3:
            luminance = image_np[..., 0] * 0.2126 + image_np[..., 1] * 0.7152 + image_np[..., 2] * 0.0722
        else:
            luminance = image_np.mean(axis=-1)
        
        # 전체 이미지의 평균 휘도를 0~1 사이 값으로 계산
        avg_luminance = float(luminance.mean())
        
        return (avg_luminance,)