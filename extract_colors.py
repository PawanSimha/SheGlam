from PIL import Image
from collections import Counter

def get_dominant_color(image_path, num_colors=5):
    try:
        img = Image.open(image_path).convert('RGBA')
        img = img.resize((100, 100))  # Resize for faster processing
        pixels = list(img.getdata())
        
        # Filter out transparent, white, and black pixels
        filtered_pixels = []
        for r, g, b, a in pixels:
            if a < 50: continue  # Transparent
            if r > 240 and g > 240 and b > 240: continue  # White-ish
            if r < 15 and g < 15 and b < 15: continue  # Black-ish
            filtered_pixels.append((r, g, b))
            
        if not filtered_pixels:
            print("No significant color found (mostly black/white/transparent). Defaulting to Black.")
            return "#000000"

        counts = Counter(filtered_pixels)
        dominant = counts.most_common(1)[0][0]
        return f"#{dominant[0]:02x}{dominant[1]:02x}{dominant[2]:02x}"
        
    except Exception as e:
        print(f"Error: {e}")
        return "#000000"

if __name__ == "__main__":
    color = get_dominant_color('frontend/static/images/SheGlam.png')
    print(f"BRAND_COLOR={color}")
