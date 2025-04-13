from flask import Flask, render_template, request, url_for
import pandas as pd
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)


def allocate_funds(received, keep_in_checking, accounts):
    available_funds = float(received - keep_in_checking)
    total_accounts = len(accounts)
    allocations = [0] * total_accounts

    # First, allocate funds to accounts with min_send requirements
    for i, account in enumerate(accounts):
        min_send = float(account.get("min_send", 0))
        if min_send > 0 and available_funds > 0:
            allocations[i] = min_send
            if available_funds <= min_send:
                allocations[i] = available_funds
            available_funds -= allocations[i]
            account["allocated"] = round(allocations[i], 2)
        else:
            account["allocated"] = 0

    # Then, allocate remaining funds to all accounts
    for i, account in enumerate(accounts):
        if available_funds > 0:
            share = available_funds / (total_accounts - i)
            allocations[i] += min(share, available_funds)
            available_funds -= min(share, available_funds)
            account["allocated"] = round(allocations[i], 2)

    df = pd.DataFrame(accounts)
    df.insert(0, "account_number", range(1, len(df) + 1))
    return df[["account_number", "name", "allocated"]].to_dict(orient="records")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/allocate", methods=["POST"])
def allocate():
    data = request.json
    received_amount = float(data["received_amount"])
    keep_amount = float(data["keep_amount"])
    accounts = data["accounts"]
    allocation_table = allocate_funds(received_amount, keep_amount, accounts)
    return {"allocation_table": allocation_table}


if __name__ == "__main__":
    app.run(debug=True)
