from flask import Flask, render_template, redirect, jsonify, request
from time import sleep

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    sleep(2)
    data = request.json
    if not validate_predict_json(data):
        return jsonify({
            'error': 'Received wrong data.'
        })
    return jsonify({
        'success': 'okay bro'
    })
    # TODO: continue here


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
    # TODO: ML init (load the data in memory)
    app.run()
