import boto3
import pandas as pd
from io import StringIO, BytesIO
from datetime import datetime, timedelta

class Extract:
    def __init__(self):
        self.arg_date = '2022-03-02'
        self.src_format = '%Y-%m-%d'
        self.src_bucket = 'deutsche-boerse-xetra-pds'
        self.trg_bucket = 'xetra-bucket-2022-03-02-gerardo'
        self.columns = ['ISIN', 'Date', 'Time', 'StartPrice', 'MaxPrice', 'MinPrice', 'EndPrice', 'TradedVolume']
        self.key = 'xetra_daily_report_' + datetime.today().strftime("%Y%m%d_%H%M%S") + '.parquet'


class Tranform:
    def __init__(self):
        pass

class Load:
    def __init__(self):
        pass