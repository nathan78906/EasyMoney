import requests
import json

auth_data = {
    "grant_type"    : "client_credentials",
    "client_id"     : "f16cd82ee1114e9aa586d8a9b9061e5d",
    "client_secret" : "51561554100c3a879a77999c21bae8fbec811421c3f33ccf4ffc562658d3498e",
    "scope"         : "read_product_data"
}

# create session instance
session = requests.Session()

auth_request = session.post("https://idfs.gs.com/as/token.oauth2", data = auth_data)
access_token_dict = json.loads(auth_request.text)
access_token = access_token_dict["access_token"]

# update session headers with access token
session.headers.update({"Authorization":"Bearer "+ access_token})

request_url = "https://api.marquee.gs.com/v1/assets/data/query"

request_query = {
                    "where": {
                        "gsid": ['75154', '193067', '194688', '902608', '85627', '13901', '150407', '161467', '85072', '82598', '86372', '11896', '230958', '177256', '49154', '76605', '173578', '85914', '193324', '75100', '149756', '213305', '79758', '69796', '81116', '202271', '79145', '84275', '183269', '76226', '18163', '80791', '152963', '197235', '227284', '222946', '85631', '25022', '61621', '59010', '902704', '216587', '901237', '80286', '77659', '15579', '53613', '16600', '75573', '216722', '46578', '75573', '53065', '84769', '13936', '46922', '905632', '13936', '193155', '91556', '64064', '79265', '151048', '176665', '46886', '183414', '70500', '16432', '905632', '173578', '86196', '11308', '55976', '188804', '226278', '26825', '183269', '172890', '905288', '29209', '188329', '10516', '75607', '18729', '16678', '44644', '223416', '82598', '26403', '91556', '59248', '78975', '903917', '78045', '12490', '40539', '148401', '17750', '198025', '10696', '22293', '66384', '85517', '217708', '79145', '85631', '86356', '905255', '14593', '85072']
                    },
                    "fields": ["gsid", "ticker", "name"],
                    "limit": 300,
                    "offset": 100
               }

request = session.post(url=request_url, json=request_query)
results = json.loads(request.text)
import pdb; pdb.set_trace();