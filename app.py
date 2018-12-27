from flask import Flask, jsonify, request
from flask import render_template

from Url2Tree import get_data

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html", domain=request.args.get('domain'))


@app.route('/json')
def get_json():
    return jsonify(get_data(request.args.get('domain')))


if __name__ == '__main__':
    app.run(debug=True)
