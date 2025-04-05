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
            # 例: custom_config = r'--oem 1 --psm 6 -c preserve_interword_spaces=1'
            # --oem (OCR Engine Mode):
            #   0: Legacy engine only
            #   1: LSTM エンジンのみを使用 (Neural Net ベースの OCRエンジン)
            #   2: Legacy + LSTM engines
            #   3: Default, based on what is available
            # --psm (Page Segmentation Mode):
            #   0: Orientation and script detection only
            #   1: Automatic page segmentation with OSD
            #   3: Fully automatic page segmentation, no OSD
            #   6: 単一の均一なテキストブロックを想定
            #   7: Single text line
            #   8: Single word
            #   10: Single character
            #   11: Sparse text
            # -c preserve_interword_spaces:
            #   0: 単語間のスペースを結合する可能性がある (デフォルト)
            #   1: 単語間のスペースを維持
            custom_config = r'--oem 1 -c preserve_interword_spaces=1'
            
            # OCR実行
            text = pytesseract.image_to_string(
                processed_image, 
                lang='jpn+jpn_vert',
                config=custom_config
            )
            all_text_list.append(text)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Create a unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 結果を分割して保存
    chunk_size = 25
    for i in range(0, len(all_text_list), chunk_size):
        part_text = "\n".join(all_text_list[i:i + chunk_size])
        part_number = i // chunk_size + 1
        part_filename = f"output/output_{timestamp}_part_{part_number}.txt"
        try:
            with open(part_filename, "w", encoding="utf-8") as part_file:
                part_file.write(part_text)
            print(f"Successfully wrote to {part_filename}")
        except Exception as e:
            print(f"Failed to write to {part_filename}: {e}")

    print(f"OCR extraction complete. Output saved to {len(all_text_list) // chunk_size + 1} parts.")

if __name__ == "__main__":
    main()
