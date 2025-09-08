import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

file_path = '/DATA/20170504T083011_20170504T083011_T36SWH__ROI_2279.tif'

with rasterio.open(file_path) as src:
    red = src.read(4)
    green = src.read(3)
    blue = src.read(2)


rgb = np.dstack((red, green, blue))

rgb_norm = rgb / np.max(rgb)


# Show image
plt.figure(figsize=(10,10))
plt.imshow(rgb_norm)
plt.axis('off')
plt.show()
