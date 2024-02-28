import threading
import pandas as pd
import numpy as np
import flask
from flask import jsonify, request

app = flask.Flask(__name__)

model = None
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
    global model

    data = request.get_json()
    artikuls = np.asarray(data)

    model_by_artikuls = model[model['Артикул'].isin(artikuls)]


    fh_list_all = model_by_artikuls['горизонт_прогнозирования'].to_numpy()  # для хранения списка горизонта прогнозирования
    artikuls_list = model_by_artikuls['Артикул'].to_numpy()  # список всех артикулов (должен быть входящим параметром)
    sales_list = model_by_artikuls.iloc[:, 3:-1].to_numpy()  # список продаж артикулов
    pred_list = np.empty(artikuls_list.shape)  # для хранения значений прогноза на день
    fh_list = np.empty(artikuls_list.shape)
    pred_list[:] = np.nan
    fh_list[:] = np.nan

    for i in range(len(artikuls_list)):  # итерация по индексам (по артикулам)
        fh = fh_list_all[i]  # горизонт прогнозирования для артикула
        sales_fh_list = sales_list[i, -fh:]  # список последних fh продаж
        pred = sales_fh_list.mean()  # среднее за день в качестве прогноза
        pred_list[i] = pred
        fh_list[i] = fh

    prediction_df = pd.DataFrame({'artikul':artikuls_list, 'prediction':pred_list, 'forcast_horizon':fh_list})


    return prediction_df.to_json(orient='index')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    model = pd.read_csv('sale_df.csv')
    app.run(host='192.168.10.21', port=5000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
