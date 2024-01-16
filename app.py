from flask import Flask, jsonify

from flask import Flask, request
from flask_restful import Api, Resource

import io

from PIL import Image
from ultralytics import YOLO
import base64

from create_json import create_json

app = Flask(__name__)
api = Api(app)


class ScreenshotResource(Resource):
    def post(self):
        xy = []
        cls = []
        # Получение данных из JSON-запроса
        data = request.get_json()

        # Проверка наличия ключа "screenshot" в JSON-данных
        if "screenshot" in data:
            screenshot_data = data["screenshot"]

            binary_data = base64.b64decode(screenshot_data)

            image = Image.open(io.BytesIO(binary_data))

            model = YOLO('best.pt')

            results = model(source=image, show=True, conf=0.6, save=True)

            boxes = results[0].boxes.xyxy.tolist()
            classes = results[0].boxes.cls.tolist()

            response_data = create_json(boxes, classes)

            return response_data, 200
        else:
            # Возвращение ошибки, если ключ "screenshot" отсутствует
            return {"error": "Missing 'screenshot' key in JSON data"}, 400


# Добавление ресурса к API
api.add_resource(ScreenshotResource, '/screenshot')

if __name__ == '__main__':
    # Запуск Flask-приложения
    app.run(debug=True)
