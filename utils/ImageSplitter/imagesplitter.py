import os
import sys
from PIL import Image

def slice_image(image_path, tile_size=16):
    # 入力ファイル名から出力ディレクトリを作成
    filename = os.path.basename(image_path)
    name, _ = os.path.splitext(filename)
    output_dir = os.path.join("out", name)
    os.makedirs(output_dir, exist_ok=True)

    # 画像を開く
    img = Image.open(image_path)
    width, height = img.size

    # 画像を16x16で分割して保存
    index = 0
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            box = (x, y, x + tile_size, y + tile_size)
            tile = img.crop(box)
            tile.save(os.path.join(output_dir, f"tile_{index}.png"))
            index += 1

    print(f"{index} tiles saved to {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python slice_tiles.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    slice_image(image_path)
