
# from flask_cors import CORS
# from flask import Flask, render_template, jsonify
# import pandas as pd

# app = Flask(__name__)


# CORS(app, resources={r"/*": {"origins": "*"}})


# @app.route("/")
# def index():
#     return render_template("index.html")


# # データ周り
# file_path = '../task_generate/GR03_contributions.csv'
# df = pd.read_csv(file_path)
# df_unique = df.drop_duplicates(subset=['address'])
# wallet_addresses = df_unique['address'].head(90).tolist()


# @app.route("/get-content")
# def get_content():
#     return jsonify(
#         initial_tasks=[wallet_addresses[i:i+6]
#                        for i in range(0, len(wallet_addresses), 6)]
#     )


# if __name__ == "__main__":
#     app.run(debug=True)


# 昼寝後の実装
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

# ウォレットアドレスと初期タスクの変数
wallet_addresses = []
initial_tasks = []


@app.route('/')
def index():
    return "Welcome to DeCartography API"

# 初期タスクを生成


@app.route('/generate_initial_tasks', methods=['POST'])
def generate_initial_tasks():
    global wallet_addresses, initial_tasks
    df = pd.read_csv('../task_generate/GR03_contributions.csv')  # CSV ファイルのパス
    df_unique = df.drop_duplicates(subset=['address'])

    # wallet_addresses = df_unique['address'].head(90).tolist()

    #実験なので、18個だけ引っ張ってくることにしておく
    wallet_addresses = df_unique['address'].head(18).tolist()

    initial_tasks = [wallet_addresses[i:i+6]
                     for i in range(0, len(wallet_addresses), 6)]
    return jsonify({"message": "Initial tasks generated", "initial_tasks": initial_tasks})

# 初期タスクを取得

@app.route('/get_initial_task/<int:task_index>', methods=['GET'])
def get_initial_task(task_index):
    if task_index < len(initial_tasks):
        return jsonify({"task": initial_tasks[task_index]})
    else:
        return jsonify({"message": "No more tasks available"}), 404


if __name__ == "__main__":
    app.run(debug=True)