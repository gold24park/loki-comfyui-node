import numpy as np
from PIL import Image

class ImageSaturation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("FLOAT",)  # 반환 타입: float (0~1 사이의 값)
    FUNCTION = "get_saturation"
    CATEGORY = "LokiComfyUINode/Image Analysis"  # 원하는 카테고리명으로 변경 가능

    def get_saturation(self, image):
        """
        입력 이미지의 채도(Saturation)를 HSV 색공간에서 계산하여 평균값(0~1)을 반환합니다.
        """
        # 입력 이미지가 PIL 이미지가 아닐 경우 numpy 배열로 가정하고 변환
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)

        # 이미지를 HSV 모드로 변환
        hsv_image = image.convert("HSV")
        # HSV 채널 분리: H, S, V 중 S(채도) 채널 추출
        _, s_channel, _ = hsv_image.split()

        # 채도 채널을 numpy 배열로 변환하고 0~1 범위로 정규화
        s_array = np.array(s_channel, dtype=np.float32) / 255.0

        # 전체 이미지에 대한 평균 채도 계산
        avg_saturation = float(np.mean(s_array))
        return (avg_saturation,)