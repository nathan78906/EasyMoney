import requests
import json
import datetime

auth_data = {
    "grant_type"    : "client_credentials",
    "client_id"     : "f16cd82ee1114e9aa586d8a9b9061e5d",
    "client_secret" : "51561554100c3a879a77999c21bae8fbec811421c3f33ccf4ffc562658d3498e",
    "scope"         : "read_product_data"
}

portfolio = {
    '213305': {'ticker': 'TSLA', 'score': 0, 'number_bought': 1},
    '149756': {'ticker': 'NFLX', 'score': 0, 'number_bought': 1},
    '227284': {'ticker': 'FB', 'score': 0, 'number_bought': 1},
    '176665': {'ticker': 'EXPE', 'score': 0, 'number_bought': 1},
    '75573': {'ticker': 'ODP', 'score': 0, 'number_bought': 1},
    '86196': {'ticker': 'ULTI', 'score': 0, 'number_bought': 1},
    '25022': {'ticker': 'CMCSA', 'score': 0, 'number_bought': 1},
    '44644': {'ticker': 'ADP', 'score': 0, 'number_bought': 1},
    '66384': {'ticker': 'WDC', 'score': 0, 'number_bought': 1},
    '86356': {'ticker': 'EBAY', 'score': 0, 'number_bought': 1},
    '161467': {'ticker': 'CRM', 'score': 0, 'number_bought': 1}
}
gsids = [gsid for gsid in portfolio]

SELL_FACTOR = -0.005
BUY_FACTOR = 0.005

# create session instance
session = requests.Session()

auth_request = session.post("https://idfs.gs.com/as/token.oauth2", data = auth_data)
access_token_dict = json.loads(auth_request.text)
access_token = access_token_dict["access_token"]

# update session headers with access token
session.headers.update({"Authorization":"Bearer "+ access_token})

request_url = "https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query"

start_date = datetime.datetime(2017, 1, 1)
end_date = datetime.datetime(2017, 1, 2)


for i in range(0, 29):
    request_query = {
                    "where": {
                        "gsid": gsids
                    },
                    "startDate": start_date.strftime("%Y-%m-%d"),
                    "endDate": end_date.strftime("%Y-%m-%d")
               }

    request = session.post(url=request_url, json=request_query)
    results = json.loads(request.text)
    print("{} - {}".format(start_date, end_date))

    for stock in results['data']:
        net = stock['integratedScore'] - portfolio[stock['gsid']]['score']
        if portfolio[stock['gsid']]['score'] == 0:
            portfolio[stock['gsid']]['score'] = stock['integratedScore']
        elif net > BUY_FACTOR:
            if portfolio[stock['gsid']]['number_bought'] < 1:
                print("Buying: {}".format(portfolio[stock['gsid']]['ticker']))
                portfolio[stock['gsid']]['score'] = stock['integratedScore']
                portfolio[stock['gsid']]['number_bought'] += 1
        elif net < SELL_FACTOR:
            if portfolio[stock['gsid']]['number_bought'] > 0:
                print("Selling: {}".format(portfolio[stock['gsid']]['ticker']))
                portfolio[stock['gsid']]['score'] = stock['integratedScore']
                portfolio[stock['gsid']]['number_bought'] -= 1
        else:
            portfolio[stock['gsid']]['score'] = stock['integratedScore']

    start_date += datetime.timedelta(days=1)
    end_date += datetime.timedelta(days=1)