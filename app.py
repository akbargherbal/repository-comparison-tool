import json
from flask import Flask, jsonify, render_template
import pandas as pd
from helpers import get_repo_json_tree


# Load and pre-process the data once on startup for efficiency
df = pd.read_parquet("./recipes_json_trees.parquet")
df["DATE"] = pd.to_datetime(df["DATE"])
df = df.sort_values(by="DATE").reset_index(drop=True)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tree/<year>/<month>")
def get_tree_data(year, month):
    """
    Returns a JSON object containing the tree data and commit metadata for the
    first commit on or after a specific year/month.
    """
    try:
        json_tree_str, date, commit_hash, github_link = get_repo_json_tree(
            df, year, month
        )
        # The 'TREE' column contains a JSON string; parse it into a Python object
        tree_data = json.loads(json_tree_str)

        # Package all data into a single JSON response
        return jsonify(
            {
                "tree": tree_data,
                "commit_hash": commit_hash,
                "date": date.isoformat(),  # Use standard ISO format
                "github_link": github_link,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
