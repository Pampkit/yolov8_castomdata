from flask import Flask, jsonify

from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource

import io

from PIL import Image
from ultralytics import YOLO
import base64
import json

from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder

from create_json import create_json

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Image Processing System",
        "description": "API Documentation for Image Processing System",
        "contact": {
            "name": "Alisa",
            "email": "alisaalborova13@gmail.com",
        },
        "termsOfService": "Terms of services",
        "version": "1.0",
        "host": "Image_Processing_System",
        "basePath": "http://localhost:5000",
        "license": {
            "name": "License of API",
            "url": "API license URL"
        }
    },
    "schemes": [
        "http",
        "https"
    ],
}

swagger_config = {
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST"),
    ],
    "specs": [
        {
            "endpoint": 'Image_Processing_System',
            "route": '/Image_Processing_System.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",

}
swagger = Swagger(app, template=swagger_template, config=swagger_config)


@swag_from("post.yaml")
@app.route("/main", methods=["POST"])
def post():
    if request.method == "POST":
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
    else:
        return {"responseCode": "1","responseDesc": "Method Not Allowed"}, 405



if __name__ == '__main__':
    # Запуск Flask-приложения
    app.run(debug=True)
