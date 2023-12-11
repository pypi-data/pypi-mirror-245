# -*- coding: utf-8 -*-

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src import investlife as iv

iv.set_token(token = 'abcd')

data = iv.get_stock_list()
# data = get_realtime_quotes()
print(data.head())
