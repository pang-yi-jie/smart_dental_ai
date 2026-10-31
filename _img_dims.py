import glob
import os
from PIL import Image

for p in glob.glob(r"D:\SmartDentalAI\_ref\images\*.png"):
    im = Image.open(p)
    w, h = im.size
    print(f"{os.path.basename(p):<24} {w}x{h}  宽高比 {w/h:.2f}")
