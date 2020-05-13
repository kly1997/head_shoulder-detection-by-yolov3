
from functools import reduce

from PIL import Image
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
image = Image.open('C://Users\86137\Desktop/111.jpg')
iw, ih = image.size
size = (416, 416)
w, h = size
scale = min(w / iw, h / ih)
nw = int(iw * scale)
nh = int(ih * scale)

image = image.resize((nw, nh), Image.BICUBIC)
new_image = Image.new('RGB', size, (128, 128, 128))
new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
new_image.show()