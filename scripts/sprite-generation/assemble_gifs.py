#!/usr/bin/env python3
"""
GIF Assembly Script for Fork Monkey
Converts generated PNG frames into animated GIFs suitable for VS Code Pets
"""

import os
from PIL import Image, ImageOps
import glob

# Configuration
FRAMES_DIR = "/home/ubuntu/forkmonkey-assets/frames"
GIFS_DIR = "/home/ubuntu/forkmonkey-assets/gifs"
TARGET_SIZE = (111, 101)  # VS Code Pets standard size
FPS = 8
FRAME_DURATION = int(1000 / FPS)  # milliseconds per frame
COLOR = "brown"  # Fork monkey color variant

# Animation definitions (must match generate_forkmonkey.py)
ANIMATIONS = {
    'idle': 4,
    'walk': 6,
    'run': 8,
    'swipe': 5,
    'with_ball': 4
}

def ensure_transparency(image):
    """Ensure image has proper transparency"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    return image

def remove_white_background(image):
    """Convert white/light backgrounds to transparent"""
    image = ensure_transparency(image)
    
    # Get image data
    data = image.getdata()
    
    new_data = []
    for item in data:
        # Change all white (also shades of whites)
        # to transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    image.putdata(new_data)
    return image

def crop_to_content(image, padding=5):
    """Crop image to actual content with padding"""
    # Get the bounding box of non-transparent pixels
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Get alpha channel
    alpha = image.split()[-1]
    bbox = alpha.getbbox()
    
    if bbox:
        # Add padding
        bbox = (
            max(0, bbox[0] - padding),
            max(0, bbox[1] - padding),
            min(image.width, bbox[2] + padding),
            min(image.height, bbox[3] + padding)
        )
        return image.crop(bbox)
    
    return image

def resize_and_center(image, target_size):
    """Resize image to fit target size while maintaining aspect ratio and center it"""
    # Ensure transparency
    image = ensure_transparency(image)
    
    # Calculate scaling to fit within target size
    width_ratio = target_size[0] / image.width
    height_ratio = target_size[1] / image.height
    scale = min(width_ratio, height_ratio)
    
    # Calculate new size
    new_width = int(image.width * scale)
    new_height = int(image.height * scale)
    
    # Resize with high-quality resampling
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create a new transparent image of target size
    final = Image.new('RGBA', target_size, (0, 0, 0, 0))
    
    # Calculate position to center the resized image
    x = (target_size[0] - new_width) // 2
    y = (target_size[1] - new_height) // 2
    
    # Paste the resized image onto the center
    final.paste(resized, (x, y), resized)
    
    return final

def process_frame(frame_path, target_size):
    """Process a single frame: load, clean, resize, center"""
    print(f"    Processing: {os.path.basename(frame_path)}")
    
    # Load image
    image = Image.open(frame_path)
    
    # Remove white background
    image = remove_white_background(image)
    
    # Crop to content
    image = crop_to_content(image, padding=10)
    
    # Resize and center
    image = resize_and_center(image, target_size)
    
    return image

def create_animated_gif(animation_name, frame_count, output_path):
    """Create an animated GIF from frames"""
    print(f"\n🎬 Creating {animation_name} animation...")
    print(f"   Frames: {frame_count}")
    
    # Find all frames for this animation
    frame_files = []
    for i in range(1, frame_count + 1):
        frame_path = os.path.join(FRAMES_DIR, f"{animation_name}_frame_{i:02d}.png")
        if os.path.exists(frame_path):
            frame_files.append(frame_path)
        else:
            print(f"   ⚠️  Warning: Frame {i} not found: {frame_path}")
    
    if not frame_files:
        print(f"   ❌ No frames found for {animation_name}")
        return False
    
    print(f"   Found {len(frame_files)} frames")
    
    # Process all frames
    processed_frames = []
    for frame_file in frame_files:
        processed_frame = process_frame(frame_file, TARGET_SIZE)
        processed_frames.append(processed_frame)
    
    # Convert to palette mode for GIF (with transparency)
    # First frame will be used as the base for palette
    gif_frames = []
    for frame in processed_frames:
        # Convert RGBA to P (palette) mode with transparency
        # Use adaptive palette for best quality
        frame_p = frame.convert('P', palette=Image.ADAPTIVE, colors=256)
        gif_frames.append(frame_p)
    
    # Save as animated GIF
    print(f"   💾 Saving to: {output_path}")
    gif_frames[0].save(
        output_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=FRAME_DURATION,
        loop=0,
        transparency=0,
        disposal=2,
        optimize=False  # Don't optimize to maintain quality
    )
    
    # Get file size
    file_size = os.path.getsize(output_path)
    print(f"   ✅ Created! Size: {file_size / 1024:.1f} KB")
    
    return True

def main():
    print("="*60)
    print("🎞️  FORK MONKEY GIF ASSEMBLY")
    print("="*60)
    
    # Create output directory
    os.makedirs(GIFS_DIR, exist_ok=True)
    print(f"📁 Output directory: {GIFS_DIR}")
    
    # Process each animation
    success_count = 0
    for anim_name, frame_count in ANIMATIONS.items():
        output_filename = f"{COLOR}_{anim_name}_8fps.gif"
        output_path = os.path.join(GIFS_DIR, output_filename)
        
        if create_animated_gif(anim_name, frame_count, output_path):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"✅ COMPLETE! {success_count}/{len(ANIMATIONS)} animations created")
    print(f"📁 Output directory: {GIFS_DIR}")
    print("="*60)
    
    # List all created GIFs
    print("\n📋 Created GIFs:")
    for gif_file in sorted(glob.glob(os.path.join(GIFS_DIR, "*.gif"))):
        size = os.path.getsize(gif_file)
        print(f"   • {os.path.basename(gif_file)} ({size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
