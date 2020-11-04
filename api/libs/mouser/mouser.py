import requests
import json


"""
m = Mouser("https://api.mouser.com/api", "1", "api-key-here)
# fetch all orders matching last month filter
orders = m.order_history.by_date_filter("LastMonth")
# get one order web number
order_number = orders['OrderHistoryItems][0]['WebOrderNumber]
# get all items in that order
items = m.order_number(order_number)
print(items)
"""


class Mouser:
    def __init__(self, base_url="https://api.mouser.com", api_version="1", api_key=None, **kwargs):
        self.base_url = base_url
        self.api_version = api_version
        self.api_key = api_key
        self.api_url = f"{self.base_url}/api/v{self.api_version}"

    @staticmethod
    def parse_and_check(data):
        errors = data["Errors"]
        if len(errors) > 0:
            raise Exception(f"Errors: {errors}")
        return data

    def request(self, url, query={}, data=None):
        params = {"apiKey": self.api_key, **query}
        headers = {"Accept": "application/json", "User-Agent": "Python/Requests StockazIO/dashie@sigpipe.me"}

        if not data:
            r = requests.get(url, headers=headers, params=params, timeout=60)
        else:
            headers.update({"Content-Type": "application/json"})
            r = requests.post(url, headers=headers, params=params, data=json.dumps(data), timeout=60)
        if r.status_code != 200:
            raise ("HTTP Response != 200")
        return r.json()

    def order_history_by_date_filter(self, filter="LastMonth"):
        if not filter:
            raise ("filter should be defined")
        url = f"{self.api_url}/orderhistory/ByDateFilter"
        params = {"dateFilter": filter}
        resp = self.request(url, query=params)
        return self.parse_and_check(resp)

    def order_number(self, order_number=None):
        if not order_number:
            raise ("order_number is required")
        url = f"{self.api_url}/order/{order_number}"
        resp = self.request(url)
        return self.parse_and_check(resp)
