import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import DetectPlate

# To change black pixel to white pixel or viceversa we use invert

#print(DetectPlate.plate_like_objects)
license_plate = np.invert(DetectPlate.plate_like_objects[0])
labelled_plate = measure.label(license_plate)
fig, ax1 = plt.subplots(1)
ax1.imshow(license_plate, cmap="gray")
#we assume that the licence plate should have height between 35% to 60% #and width between 5 to 15%
ch_dim = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.04*license_plate.shape[1], 0.12*license_plate.shape[1])
min_h, max_h, min_w, max_w = ch_dim

ch = []
g=0
col_l = []
for regions in regionprops(labelled_plate):
    y0, x0, y1, x1 = regions.bbox
    region_h = y1 - y0
    region_w = x1 - x0

    if region_h > min_h and region_h < max_h and region_w > min_w and region_w < max_w:
        roi = license_plate[y0:y1, x0:x1]

        #to draw a rectangle over the character having red border
        rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rect_border)

        # resizing to 20x20 and adding each character in characters list
        resized_ch = resize(roi, (20, 20))
        ch.append(resized_ch)

        # it is used to track arrangement of characters
        col_l.append(x0)
#print(ch)
plt.show()
