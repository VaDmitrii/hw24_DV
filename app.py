from flask import Flask, request, jsonify

from utils import result_data

app = Flask(__name__)


@app.route("/perform_query")
def perform_query():
    try:
        file_name: str = request.args.get('file_name')
        cmd1: str = request.args.get('cmd1')
        value1: str = request.args.get('value1')
        cmd2: str = request.args.get('cmd2')
        value2: str = request.args.get('value2')
    except (KeyError, ValueError) as error:
        return jsonify(error.messages), 400
    commands_list: dict = {cmd1: value1, cmd2: value2}
    result = result_data(file_name, commands_list)
    get_result: list = list(result)
    return jsonify(get_result)


if __name__ == '__main__':
    app.run()
