import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import colorsys


class DominantColor:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "image": ("IMAGE",),
                "num_colors": ("INT", {"default": 1, "min": 1, "max": 10}),
                "find_bright": ("BOOLEAN", {"default": False}),
            }
        }
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("hex_color",)
    FUNCTION = "get_dominant_color"
    OUTPUT_NODE = True
    CATEGORY = "LokiComfyUINode/Image Analysis"
    
    def is_brightness_match(self, rgb_color, find_bright):
        if find_bright:
            min_brightness = 0.5
            max_brightness = 1.0
        else:
            min_brightness = 0.0
            max_brightness = 0.5
            
        # Convert RGB to HSV
        r, g, b = rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        # Check if the color's value (brightness) is below the threshold
        return v >= min_brightness and v <= max_brightness
    
    def get_dominant_color(self, image, num_colors=1, find_bright=False):
        # Convert the tensor to PIL Image
        if len(image.shape) == 4:
            image = image[0]
        
        # Convert to numpy array and reshape
        image_array = (image * 255).cpu().numpy().astype(np.uint8)
        h, w, _ = image_array.shape
        image_array_reshaped = image_array.reshape((h * w, 3))
        
        # Use KMeans to find more clusters than requested to ensure we have enough dark colors
        kmeans = KMeans(n_clusters=min(num_colors * 3, h * w, 10), random_state=42) # 최대 10개로 제한
        kmeans.fit(image_array_reshaped)
        
        # Get the dominant colors and filter dark ones
        colors = kmeans.cluster_centers_
        match_colors = [color for color in colors if self.is_brightness_match(color, find_bright)]
        
        if len(match_colors) == 0:
            match_colors = colors
        
        # Sort dark colors by frequency (using cluster labels)
        color_frequencies = np.bincount(kmeans.labels_)
        dark_color_indices = [i for i, color in enumerate(colors) if self.is_brightness_match(color, find_bright)]
        match_colors_with_freq = [(colors[i], color_frequencies[i]) for i in dark_color_indices]
        match_colors_with_freq.sort(key=lambda x: x[1], reverse=True)
        
        # Take the requested number of dark colors
        final_colors = [color for color, _ in match_colors_with_freq[:num_colors]]
        
        if not final_colors:
            return (colors[0],)  # Return the first color if no colors found
            
        # Convert to hex color codes
        hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(c[0]), int(c[1]), int(c[2])) 
                     for c in final_colors]
        
        return (hex_colors[0] if num_colors == 1 else ', '.join(hex_colors),)