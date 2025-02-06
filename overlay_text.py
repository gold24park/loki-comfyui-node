import numpy as np
import torch
import os
import platform
from .functions_graphics import *
from .config import color_mapping, COLORS
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter, ImageColor

ALIGN_OPTIONS = ["center", "top", "bottom"]
ROTATE_OPTIONS = ["text center", "image center"]
JUSTIFY_OPTIONS = ["center", "left", "right"]
PERSPECTIVE_OPTIONS = ["top", "bottom", "left", "right"]

class OverlayText:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

        return {"required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (COLORS,),
                "align": (ALIGN_OPTIONS,),
                "justify": (JUSTIFY_OPTIONS,),
                "margins": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "line_spacing": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                "rotation_options": (ROTATE_OPTIONS,),
                "letter_spacing": ("FLOAT", {"default": 0.0, "min": -100.0, "max": 100.0}),
                },
                "optional": {
                    "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "shadow": ("BOOLEAN", {"default": False}),
                    "shadow_offset_x": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                    "shadow_offset_y": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                    "shadow_color_hex": ("STRING", {"default": "#000000"}),
                    "shadow_opacity": ("INT", {"default": 128, "min": 0, "max": 255}),
                    "shadow_blur": ("INT", {"default": 5, "min": 0, "max": 100}),
                }
    }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "overlay_text"
    CATEGORY = "LokiComfyUINode/Text"

    def overlay_text(self, image, text, font_name, font_size, font_color,
                     margins, line_spacing,
                     position_x, position_y,
                     align, justify,
                     rotation_angle, rotation_options,
                     letter_spacing,
                     font_color_hex='#000000',
                     shadow=False,
                     shadow_offset_x=0,
                     shadow_offset_y=0,
                     shadow_color_hex='#00ff00',
                     shadow_opacity=128,
                     shadow_blur=5):

        # Get RGB values for the text color
        text_color = get_color_values(font_color, font_color_hex, color_mapping)

        # Convert tensor images
        image_3d = image[0, :, :, :]

        # Create PIL images for the text and background layers and text mask
        back_image = tensor2pil(image_3d)
        text_image = Image.new('RGB', back_image.size, text_color)
        text_mask = Image.new('L', back_image.size)

        # Draw the text on the text mask
        rotated_text_mask = draw_masked_text(text_mask, text, font_name, font_size,
                                             margins, line_spacing,
                                             position_x, position_y,
                                             align, justify,
                                             rotation_angle, rotation_options,
                                             letter_spacing)

        if shadow:
            # 그림자 전용 마스크를 만든다 (원본 마스크를 복사)
            shadow_mask = rotated_text_mask.copy()
            # 그림자 마스크를 offset하여 그림자가 생긴 것처럼 만든다
            shadow_mask = ImageChops.offset(shadow_mask, shadow_offset_x, shadow_offset_y)
            
            # 가우시안 블러
            shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(shadow_blur))
            
            # 그림자용 이미지 생성 (검정 또는 임의의 shadow_color, RGBA로 만들어 투명도 조절)
            shadow_color = ImageColor.getrgb(shadow_color_hex)
            shadow_image = Image.new('RGBA', back_image.size, shadow_color + (shadow_opacity,))
            
            # 배경(back_image)에 그림자를 합성
            # composite 시, 마스크가 흰색인 부분에만 shadow_image가 합성된다
            back_image = Image.alpha_composite(back_image.convert('RGBA'), Image.composite(shadow_image, Image.new('RGBA', back_image.size, (0,0,0,0)), shadow_mask))
        
        
        text_image_rgba = text_image.convert('RGBA')
        # 텍스트 마스크도 흰색=255 부분만 불투명
        mask_rgba = rotated_text_mask.convert('L')
        final_image = Image.alpha_composite(back_image.convert('RGBA'),
                                            Image.composite(text_image_rgba,
                                                            Image.new('RGBA', back_image.size, (0,0,0,0)),
                                                            mask_rgba))

        # # Composite the text image onto the background image using the rotated text mask
        # image_out = Image.composite(text_image, back_image, rotated_text_mask)

        # Convert the PIL image back to a torch tensor
        return (pil2tensor(final_image),)