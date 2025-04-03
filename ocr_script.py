import os
import sys
from PIL import Image
import pytesseract
import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr_script.py <directory>")
        sys.exit(1)
        
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Provided path is not a valid directory.")
        sys.exit(1)
    
    # Supported image extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    
    # List and sort image files in ascending order
    images = sorted([os.path.join(directory, f) for f in os.listdir(directory)
                     if f.lower().endswith(image_extensions)])
    
    all_text = ""
    for idx, image_path in enumerate(images, start=1):
        print(f"Processing image {idx}/{len(images)}")
        try:
            text = pytesseract.image_to_string(Image.open(image_path), lang='jpn+jpn_vert')
            all_text += text + "\n"
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Create a unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"output/output_{timestamp}.txt"
    
    with open(output_filename, "w", encoding="utf-8") as out_file:
        out_file.write(all_text)
    
    print(f"OCR extraction complete. Output saved to {output_filename}.")

if __name__ == "__main__":
    main()
