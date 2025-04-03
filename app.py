import sys
import pytesseract
from PIL import Image

def image_to_text(image_path):
    # 画像を読み込む
    img = Image.open(image_path)

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

    # TesseractでOCRを実行
    text = pytesseract.image_to_string(img, lang='jpn+jpn_vert', config=custom_config)

    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]  # コマンドライン引数から画像ファイルのパスを取得
        text = image_to_text(image_path)
        print(text)
    else:
        print("Usage: python app.py <path_to_image>")
