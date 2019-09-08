from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plot

import cv2
capture = cv2.VideoCapture('./video12.mp4')
count = 0
while capture.isOpened():
    value,frame = capture.read()
    if value == True:
        cv2.imshow('window-name',frame)
        cv2.imwrite("./output/frame%d.jpg" % count, frame)
        count = count + 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        break
capture.release()
cv2.destroyAllWindows()

# car image is now converted to grayscale image and then to binary image
import imutils
image_car = imread("./output/frame%d.jpg"%(count-1), as_gray=True)
image_car = imutils.rotate(image_car,270)
# image_car = imread("car.png", as_gray=True)
# it should be a 2 dimensional array
print(image_car.shape)

# the next line is not compulsory however, a grey scale pixel
# in skimage ranges between 0 & 1. multiplying it with 255
# will make it range between 0 & 255 (something we can relate better with

gray_image_car = image_car * 255
fig, (ax1, ax2) = plot.subplots(1, 2)
ax1.imshow(gray_image_car, cmap="gray")
threshold_value = threshold_otsu(gray_image_car)
binary_image_car = gray_image_car > threshold_value
# print(binary_image_car)
ax2.imshow(binary_image_car, cmap="gray")
# ax2.imshow(gray_image_car, cmap="gray")
plot.show()

# CCA (finding connected regions) of binary image


from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plot
import matplotlib.patches as patches

# this gets all the connected regions and groups them together
label_img = measure.label(binary_image_car)

print(label_img.shape[0]) #height of car image
print(label_img.shape[1]) #width of car image

# getting the maximum width, height and minimum width and height that a license plate can be
plate_dimensions = (0.03*label_img.shape[0], 0.08*label_img.shape[0], 0.15*label_img.shape[1], 0.3*label_img.shape[1])
plate_dimensions2 = (0.08*label_img.shape[0], 0.2*label_img.shape[0], 0.15*label_img.shape[1], 0.3*label_img.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []

fig, (ax1) = plot.subplots(1)
ax1.imshow(gray_image_car, cmap="gray")
flag =0
# regionprops creates a list of properties of all the labelled regions
for region in regionprops(label_img):
    # print(region)
    if region.area < 50:
        #if the region is so small then it's likely not a license plate
        continue
        # the bounding box coordinates
    min_row, min_col, max_row, max_col = region.bbox
    # print(min_row)
    # print(min_col)
    # print(max_row)
    # print(max_col)

    region_height = max_row - min_row
    region_width = max_col - min_col
    # print(region_height)
    # print(region_width)

    # ensuring that the region identified satisfies the condition of a typical license plate
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        flag = 1
        plate_like_objects.append(binary_image_car[min_row:max_row,min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",linewidth=3, fill=False)
        ax1.add_patch(rectBorder)
        # let's draw a red rectangle over those regions
if(flag == 1):
    # print(plate_like_objects[0])
    plot.show()

if(flag==0):
    min_height, max_height, min_width, max_width = plate_dimensions2
    plate_objects_cordinates = []
    plate_like_objects = []

    fig, (ax1) = plot.subplots(1)
    ax1.imshow(gray_image_car, cmap="gray")

    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_img):
        if region.area < 50:
            #if the region is so small then it's likely not a license plate
            continue
            # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        # print(min_row)
        # print(min_col)
        # print(max_row)
        # print(max_col)

        region_height = max_row - min_row
        region_width = max_col - min_col
        # print(region_height)
        # print(region_width)

        # ensuring that the region identified satisfies the condition of a typical license plate
        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            # print("hello")
            plate_like_objects.append(binary_image_car[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(rectBorder)
            # let's draw a red rectangle over those regions
    # print(plate_like_objects[0])
    plot.show()
