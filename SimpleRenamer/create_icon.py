"""
Optional script to generate icon.png for the SimpleRenamer plugin
Requires Pillow: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a 32x32 image with white background
    img = Image.new('RGB', (32, 32), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple 'R' letter
    # Try to use a default font, fallback to basic drawing if not available
    try:
        # Try to use a system font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            # Fallback: use default font
            font = ImageFont.load_default()
    
    # Draw 'R' in black
    draw.text((8, 4), 'R', fill='black', font=font)
    
    # Save as icon.png
    img.save('icon.png')
    print("icon.png created successfully!")
    
except ImportError:
    print("Pillow not installed. Install it with: pip install Pillow")
    print("Or create icon.png manually: 32x32 PNG with a simple 'R' letter")
except Exception as e:
    print(f"Error creating icon: {e}")
    print("You can create icon.png manually: 32x32 PNG with a simple 'R' letter")
