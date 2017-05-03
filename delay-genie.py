from delay_predictor import main
from flask import Flask, render_template, redirect, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if not validate_predict_json(data):
        return jsonify({
            'error': 'Received wrong data.'
        })
    result = main.predict(data)
    return jsonify(result)


@app.route('/<path>')
def catch_all(path):
    return redirect('/')


def validate_predict_json(json_dict):
    if 'departure' in json_dict and 'arrival' in json_dict and 'date' in json_dict:
        d = json_dict.get('departure')
        a = json_dict.get('arrival')
        return 'lon' in d and 'lat' in d and 'lon' in a and 'lat' in a
    else:
        return False


if __name__ == '__main__':
    main.init()
    app.run()
