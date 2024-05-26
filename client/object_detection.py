from ultralytics import YOLO
import cv2

# Having problems with making the image grayscale and maintaining channels



path = "C:/Users/sams4/Downloads/temp3.png"
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
detection_model = 'client/grid_model.pt'
model = YOLO(detection_model)

print(image.shape)
x, y = image.shape
image.reshape((x,y,3))


def process(image):
    results = model(image)

    print("Processed")
    for result in results:

        result.show()

        x1, y1, x2, y2 = result.boxes.xyxy[0].tolist()

        # Rounding the corners
        round_int = lambda x: int(round(x))
        x1 = round_int(x1)
        x2 = round_int(x2)
        y1 = round_int(y1)
        y2 = round_int(y2)


        # Cropping the image
        cropped_img = image[y1:y2, x1:x2]

        # Stretching the image
        resized_image = cv2.resize(cropped_img, (576, 576)) 

        cv2.imshow('',resized_image)

        cv2.waitKey(0)

process(image)

