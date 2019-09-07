import requests
import json
import datetime
from messenger import sendText
from whatsapp import sendToWhatsApp

auth_data = {
    "grant_type"    : "client_credentials",
    "client_id"     : "f16cd82ee1114e9aa586d8a9b9061e5d",
    "client_secret" : "51561554100c3a879a77999c21bae8fbec811421c3f33ccf4ffc562658d3498e",
    "scope"         : "read_product_data"
}

portfolio = {
    '213305': {'ticker': 'TSLA', 'name': 'Tesla Inc', 'score': 0, 'number_bought': 1},
    '149756': {'ticker': 'NFLX', 'name': 'Netflix Inc', 'score': 0, 'number_bought': 1},
    '227284': {'ticker': 'FB', 'name': 'Facebook Inc-Class A', 'score': 0, 'number_bought': 1},
    '176665': {'ticker': 'EXPE', 'name': 'Expedia Group Inc', 'score': 0, 'number_bought': 1},
    '75573': {'ticker': 'ODP', 'name': 'Office Depot Inc', 'score': 0, 'number_bought': 1},
    '86196': {'ticker': 'ULTI', 'name': 'Ultimate Software Group Inc', 'score': 0, 'number_bought': 1},
    '25022': {'ticker': 'CMCSA', 'name': 'Comcast Corp-Class A', 'score': 0, 'number_bought': 1},
    '44644': {'ticker': 'ADP', 'name': 'Automatic Data Processing', 'score': 0, 'number_bought': 1},
    '66384': {'ticker': 'WDC', 'name': 'Western Digital Corp', 'score': 0, 'number_bought': 1},
    '86356': {'ticker': 'EBAY', 'name': 'Ebay Inc', 'score': 0, 'number_bought': 1},
    '161467': {'ticker': 'CRM', 'name': 'Salesforce.com Inc', 'score': 0, 'number_bought': 1}
}
gsids = [gsid for gsid in portfolio]

SELL_FACTOR = -0.001
BUY_FACTOR = 0.001

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


for i in range(0, 100):
    print("{} - {}".format(start_date, end_date))
    user_input = input("Press enter to continue (or q to quit): ")
    if user_input == 'q':
        exit()
    request_query = {
                    "where": {
                        "gsid": gsids
                    },
                    "startDate": start_date.strftime("%Y-%m-%d"),
                    "endDate": end_date.strftime("%Y-%m-%d")
               }

    request = session.post(url=request_url, json=request_query)
    results = json.loads(request.text)

    send_to_user = ""
    buying = ""
    selling = ""

    for stock in results['data']:
        net = stock['financialReturnsScore'] - portfolio[stock['gsid']]['score']
        if portfolio[stock['gsid']]['score'] == 0:
            portfolio[stock['gsid']]['score'] = stock['financialReturnsScore']
        elif net > BUY_FACTOR:
            if portfolio[stock['gsid']]['number_bought'] < 1:
                buying += "{} ({})\n".format(portfolio[stock['gsid']]['ticker'], portfolio[stock['gsid']]['name'])
                portfolio[stock['gsid']]['score'] = stock['financialReturnsScore']
                portfolio[stock['gsid']]['number_bought'] += 1
        elif net < SELL_FACTOR:
            if portfolio[stock['gsid']]['number_bought'] > 0:
                selling += "{} ({})\n".format(portfolio[stock['gsid']]['ticker'], portfolio[stock['gsid']]['name'])
                portfolio[stock['gsid']]['score'] = stock['financialReturnsScore']
                portfolio[stock['gsid']]['number_bought'] -= 1
        else:
            portfolio[stock['gsid']]['score'] = stock['financialReturnsScore']

    if buying:
        send_to_user += "\nBuying: \n"
        send_to_user += buying.rstrip("\n")
    if selling:
        send_to_user += "\nSelling: \n"
        send_to_user += selling.rstrip("\n")

    if send_to_user:
        print(send_to_user)
        # sendText(send_to_user)
        sendToWhatsApp(send_to_user)
    start_date += datetime.timedelta(days=1)
    end_date += datetime.timedelta(days=1)