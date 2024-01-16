import io

from PIL import Image
from ultralytics import YOLO
import base64

from create_json import create_json

#
# # Convert the image to base64 format
# with open("photo_2024-01-15_12-42-05.jpg", "rb") as f:
#     encoded_image = base64.b64encode(f.read())
#     print(encoded_image)
#
# # Декодирование base64 в бинарные данные
# binary_data = base64.b64decode(encoded_image)
# print(binary_data)
#
# image = Image.open(io.BytesIO(binary_data))


model = YOLO('best.pt')

results = model(source="1.jpg", show=True, conf=0.6, save=True)

boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()

# print('Boxes: ', boxes)
# print('classes: ', classes)

print(create_json(boxes,classes))

