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

    def read_csv_to_df(filename, bucket):
        csv_obj = bucket.Object(key=filename).get().get('Body').read().decode('utf-8')
        data = StringIO(csv_obj)
        df = pd.read_csv(data, delimiter=',')
        return df

    def write_df_to_s3(trg_bucket, key, df_all, s3):
        out_buffer = BytesIO()
        df_all.to_parquet(out_buffer, index=False)
        bucket_target = s3.Bucket(trg_bucket)
        bucket_target.put_object(Body=out_buffer.getvalue(), Key=key)
        return bucket_target

    def return_objects(src_bucket, src_format,arg_date, bucket):
        arg_date_dt = datetime.strptime(arg_date, src_format).date() - timedelta(days=1)
        objects = [obj for obj in bucket.objects.all() if datetime.strptime(obj.key.split('/')[0], src_format).date() >= arg_date_dt]
        ##objKey= obj.key
        return objects

class Tranform:
    def __init__(self):
        pass

class Load:
    def __init__(self):
        pass