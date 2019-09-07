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

request_url = "https://api.marquee.gs.com/v1/data/USCANFPP_MINI/query"

request_query = {
                    "where": {
                        "gsid": ["75154", "193067", "194688", "902608", "85627"]
                    },
                    "startDate": "2017-01-15",
                    "endDate":"2018-01-15"
               }

request = session.post(url=request_url, json=request_query)
results = json.loads(request.text)
import pdb; pdb.set_trace();