import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class DominantColor:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "required": {
                "image": ("IMAGE",)
            }
        }
        return inputs

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("hex_color",)
    FUNCTION = "get_dominant_color"
    OUTPUT_NODE = True
    CATEGORY = "LokiComfyUINode/Image Analysis"
    
    def get_dominant_color(self, image, num_colors=1):
        # Convert the tensor to PIL Image
        if len(image.shape) == 4:
            image = image[0]
        
        # Convert to numpy array and reshape
        image_array = (image * 255).cpu().numpy().astype(np.uint8)
        h, w, _ = image_array.shape
        image_array_reshaped = image_array.reshape((h * w, 3))
        
        # Use KMeans to find the clusters of colors
        kmeans = KMeans(n_clusters=num_colors, random_state=42)
        kmeans.fit(image_array_reshaped)
        
        # Get the dominant colors
        colors = kmeans.cluster_centers_
        
        # Convert to hex color codes
        hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(c[0]), int(c[1]), int(c[2])) 
                     for c in colors]
        
        return (hex_colors[0] if num_colors == 1 else ', '.join(hex_colors),)