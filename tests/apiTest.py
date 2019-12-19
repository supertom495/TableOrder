import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import requests
import json
import api


def post_data(data):
    # Func post_data: Used to post data.
    # Return: Response.

    data = json.dumps(data)
    header = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        "http://kidsnparty.com.au/roben_api/table_order/public/api/stockoption", data=data, headers=header).text
    return response


url = "http://kidsnparty.com.au/roben_api/table_order/public/api/stockoption"
data = {"table": "stock_extra", "rows": [[1, 2], [1, 3], [1, 4], [2, 3]]}
# app_json = json.dumps(data)

a = api.addOption(data)
print(a)
