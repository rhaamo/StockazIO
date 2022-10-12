import json

import requests


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
        # https://api.mouser.com/api/docs/ui/index
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
        """
        Example result:
        {
            "Errors": [],
            "NumberOfOrders": 2,
            "OrderHistoryItems": [
                {
                "DateCreated": "2020-10-12T00:00:00",
                "SalesOrderNumber": "987654321",
                "WebOrderNumber": "12345678",
                "PoNumber": "12345678",
                "BuyerName": "Fluffy Otter",
                "OrderStatusDisplay": "COMPLETE"
                },
                {
                "DateCreated": "2020-10-03T00:00:00",
                "SalesOrderNumber": "654321876",
                "WebOrderNumber": "23456789",
                "PoNumber": "23456789",
                "BuyerName": "Fluffy Otter",
                "OrderStatusDisplay": "COMPLETE"
                }
            ]
        }
        """
        allowed_filters = [
            "None",
            "All",
            "Today",
            "Yesterday",
            "ThisWeek",
            "LastWeek",
            "ThisMonth",
            "LastMonth",
            "ThisQuarter",
            "LastQuarter",
            "ThisYear",
            "LastYear",
            "YearToDate",
        ]
        if filter not in allowed_filters:
            raise ("filter should be defined")

        url = f"{self.api_url}/orderhistory/ByDateFilter"
        params = {"dateFilter": filter}
        resp = self.request(url, query=params)

        return self.parse_and_check(resp)

    def order_number(self, order_number=None):
        """
        Example result:
        {
            "OrderLines": [
                {
                "Errors": [],
                "MouserATS": 0,
                "Quantity": 10,
                "PartsPerReel": 0,
                "ScheduledReleases": null,
                "InfoMessages": null,
                "MouserPartNumber": "595-TL074CN",
                "MfrPartNumber": "TL074CN",
                "Description": "Operational Amplifiers - Op Amps JFET Input Low Noise",
                "CartItemCustPartNumber": "",
                "UnitPrice": 0.455,
                "ExtendedPrice": 4.55,
                "LifeCycle": "",
                "Manufacturer": "Texas Instruments",
                "SalesMultipleQty": 0,
                "SalesMinimumOrderQty": 0
                },
                ... snip ... others items here ...
                ],
            "CurrencyCode": "EUR",
            "MerchandiseTotal": 76.54,
            "OrderTotal": 91.85,
            "OrderType": null,
            "CartGUID": "",
            "BillingAddress": {
                "Error": null,
                "AddressLocationTypeID": 1,
                "CountryCode": "FR",
                "FirstName": "Squeaky",
                "LastName": "Otter",
                "AttentionLine": "",
                "Company": "",
                "AddressOne": "42 street squeak",
                "AddressTwo": "",
                "City": "Somewhere",
                "StateOrProvince": "",
                "PostalCode": "12345",
                "PhoneNumber": "0102020321",
                "PhoneExtension": "",
                "EmailAddress": "squeak@example.fr"
            },
            "ShippingAddress": {
                ... snip ... same bloc as BillingAddress ...
            },
            "ShippingMethod": {
                "Error": null,
                "PrimaryCode": 85,
                "SecondaryCode": 0,
                "PrimaryMethod": "FedEx International Priority",
                "SecondaryMethod": "",
                "PrimaryShippingRate": null,
                "SecondaryShippingRate": null,
                "PrimaryFreightCollectAccount": "",
                "SecondaryFreightCollectAccount": ""
            },
            "PaymentMethod": {
                "Error": null,
                "PONumber": null,
                "Method": 31,
                "Name": "Visa",
                "VatAccountNumber": null,
                "VatInvoiceAddress": null
            },
            "TaxAmount": 15.31,
            "OrderID": "xxx",
            "TaxCertificateId": null,
            "Errors": [],
            "SubmitOrder": false,
            "IECCode": null
        }
        """
        if not order_number:
            raise ("order_number is required")

        url = f"{self.api_url}/order/{order_number}"
        resp = self.request(url)

        return self.parse_and_check(resp)
