from flask import Flask, request
import os
from ibm_watson import VisualRecognitionV3
import json

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


@app.route('/')
def root():
    return app.send_static_file('index.html')

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
            classifier_ids=["food"],  # ここでClassification ID を指定
            accept_language='ja').get_result()
        return json.dumps(classes)
    return


if __name__ == "__main__":
    if app.config["HOST"]:
        app.run(debug=app.config["DEBUG"], host='0.0.0.0', port=app.config["PORT"], threaded=True)
    else:
        app.run(debug=app.config["DEBUG"], port=app.config["PORT"], threaded=True)
