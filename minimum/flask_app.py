
from flask_cors import CORS
from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    return render_template("index.html")


# データ周り
file_path = '../task_generate/GR03_contributions.csv'
df = pd.read_csv(file_path)
df_unique = df.drop_duplicates(subset=['address'])
wallet_addresses = df_unique['address'].head(90).tolist()


@app.route("/get-content")
def get_content():
    return jsonify(
        initial_tasks=[wallet_addresses[i:i+6]
                       for i in range(0, len(wallet_addresses), 6)]
    )


if __name__ == "__main__":
    app.run(debug=True)
