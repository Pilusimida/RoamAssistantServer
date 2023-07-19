import json

from flask import Flask, request
from static import *
from static.Scheduling import scheduling

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name')  # 获取名为'name'的参数值
    return f'Hello, {name}!' if name else 'Hello, World!'


@app.route('/travelplanner', methods=['GET'])
def travel_planner():
    departure = request.args.get('dep')
    destination = request.args.get('des')
    duration = request.args.get('dur')
    begin_date = request.args.get('beg')

    tp = scheduling(departure, destination, int(duration), begin_date)

    return json.loads(tp.toJSON())


if __name__ == '__main__':
    app.run()
