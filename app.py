# GS Quant documentation available at:
# https://developer.gs.com/docs/gsquant/guides/getting-started/

import datetime

from gs_quant.data import Dataset
from gs_quant.session import GsSession, Environment

GsSession.use(Environment.PROD, 'f16cd82ee1114e9aa586d8a9b9061e5d', '51561554100c3a879a77999c21bae8fbec811421c3f33ccf4ffc562658d3498e', ('read_product_data'))

ds = Dataset('USCANFPP_MINI')
data = ds.get_data(datetime.date(2017, 1, 15), datetime.date(2018, 1, 15), gsid=["75154", "193067", "194688", "902608", "85627"])
print(data.head()) # peek at first few rows of data