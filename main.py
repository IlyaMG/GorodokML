import threading
import flask
from flask import jsonify, request

app = flask.Flask(__name__)

status = "None"

def async_training():
    global model
    global status

@app.route("/training", methods=["GET"])
def training():
    global status
    if status == "None" or status == "Сompleted":
        thr1 = threading.Thread(target=async_training)
        thr1.start()

    return "Training started"

@app.route("/status", methods=["GET"])
def getstatus():
    global status
    return status


@app.route("/predict", methods=["POST"])
def predict():
    result = ""
    return jsonify(result)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='192.168.10.21', port=5000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
