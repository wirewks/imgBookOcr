import os
import sys
from PIL import Image
import pytesseract
import datetime

def preprocess_image(image):
    # グレースケール変換
    image = image.convert('L')
    return image

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
    
    # Replace string accumulation with a list for better join performance
    all_text_list = []
    for idx, image_path in enumerate(images, start=1):
        print(f"Processing image {idx}/{len(images)}")
        try:
            # 画像を開いて前処理
            image = Image.open(image_path)
            processed_image = preprocess_image(image)
            
            # 最適化された設定
            custom_config = r'--oem 1 --psm 6 -c preserve_interword_spaces=1'
            
            # OCR実行
            text = pytesseract.image_to_string(
                processed_image, 
                lang='jpn+jpn_vert',
                config=custom_config
            )
            all_text_list.append(text)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    # 結果を結合
    all_text = "\n".join(all_text_list)
    
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
