from PIL import Image, ImageDraw, ImageFont
import os

def create_icons():
    # Create icons directory
    icons_dir = os.path.join('phishing-detector-extension', 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    # Correct sizes for Chrome extension
    sizes = [16, 48, 128]  # NOT 19!
    
    for size in sizes:
        # Create green background
        img = Image.new('RGBA', (size, size), (76, 175, 80, 255))  # #4CAF50
        draw = ImageDraw.Draw(img)
        
        # Draw shield shape (simplified for small sizes)
        if size == 16:
            # For 16x16 - just a simple shield outline
            draw.rectangle([4, 4, 12, 12], fill='white')
        elif size == 48:
            # For 48x48 - shield with basic shape
            shield_points = [
                (12, 16), (24, 8), (36, 16), 
                (36, 32), (24, 40), (12, 32)
            ]
            draw.polygon(shield_points, fill='white')
        else:  # 128x128
            # For 128x128 - detailed shield
            shield_points = [
                (32, 48), (64, 16), (96, 48),
                (96, 80), (64, 112), (32, 80)
            ]
            draw.polygon(shield_points, fill='white')
            # Add checkmark
            draw.line([(48, 64), (60, 80), (80, 48)], 
                     fill='#4CAF50', width=6)
        
        # Save
        img.save(os.path.join(icons_dir, f'icon{size}.png'))
        print(f"✅ Created icon{size}.png ({size}x{size})")

if __name__ == "__main__":
    create_icons()