import base64
from io import BytesIO
from flask import Flask, request
import os
from ibm_watson import VisualRecognitionV3
import json
from PIL import Image, ImageDraw,ImageFont

VISUAL_RECOGNITION_BIND_PATH = '/opt/vr-service-bind/binding'

app = Flask(__name__, static_url_path='')
app.config.from_object('config.default')
if os.getenv('APP_CONFIG_FILE'):
    app.config.from_envvar('APP_CONFIG_FILE')


visual_recognition = VisualRecognitionV3(
    version='2018-03-19'
)

if os.path.exists(VISUAL_RECOGNITION_BIND_PATH): # For IKS
    with open(VISUAL_RECOGNITION_BIND_PATH, 'r') as conffile:
        confData = json.load(conffile)
        visual_recognition = VisualRecognitionV3(
            version='2018-03-19',
            iam_apikey= confData['apikey']
        )

FONTPATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf' # for docker image
if os.getenv('PLATFORM') == 'MAC':
    FONTPATH = '/Library/Fonts/Arial.ttf'
if os.getenv('PLATFORM') == 'WINDOWS':
    FONTPATH = 'Arial.ttf'


def draw_face_area(image_file, face_detect_res):
    if len(face_detect_res) < 1:
        print('No face detection')
        return None

    image = Image.open(image_file)

    draw = ImageDraw.Draw(image, "RGBA")

    for i, faceinfo in enumerate(face_detect_res):
        x0 = faceinfo['face_location']['left']
        x1 = x0 + faceinfo['face_location']['width']
        y0 = faceinfo['face_location']['top']
        y1 = y0 + faceinfo['face_location']['height']

        font_size = 20
        font = ImageFont.truetype(FONTPATH, font_size)
        text_size = draw.textsize('88', font=font)
        if not (x1 - x0 < text_size[0] or y1 - y0 < text_size[1]):
            while x1 - x0 > text_size[0] or y1 - y0 > text_size[1]:
                font = ImageFont.truetype(FONTPATH, font_size)
                text_size = draw.textsize('88', font=font)
                font_size += 1

        font = ImageFont.truetype(FONTPATH, font_size)
        draw.rectangle(xy=(x0, y0, x1, y1), outline=(0, 249, 0))
        draw.text(xy=(x0 + 5, y0 + 5), text=str(i), fill=(0, 249, 0), font=font)

    buffer = BytesIO()  # メモリ上への仮保管先を生成
    image.save(buffer, format="PNG")  # pillowのImage.saveメソッドで仮保管先へ保存

    base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")

    return base64Img


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/detectFaces', methods=['POST'])
def detectFaces():
    file = request.files['file']
    if file:
        classes = visual_recognition.detect_faces(
            file,
            threshold='0.6',
            accept_language='ja').get_result()
        classes['base64img'] = draw_face_area(file, classes['images'][0]['faces'])
        return json.dumps(classes)
    return


@app.route('/classifyImages', methods=['POST'])
def classifyImages():
    file = request.files['file']
    if file:
        classes = visual_recognition.classify(
            file,
            threshold='0.6',
            accept_language='ja').get_result()
        return json.dumps(classes)
    return


@app.route('/classifyCustomImages', methods=['POST'])
def classifyCustomImages():
    file = request.files['file']
    if file:
        classes = visual_recognition.classify(
            file,
            threshold='0.6',
            classifier_ids=["food"],  # ここでfoodを指定
            accept_language='ja').get_result()
        return json.dumps(classes)
    return


if __name__ == "__main__":
    if app.config["HOST"]:
        app.run(debug=app.config["DEBUG"], host='0.0.0.0', port=app.config["PORT"], threaded=True)
    else:
        app.run(debug=app.config["DEBUG"], port=app.config["PORT"], threaded=True)
