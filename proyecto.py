import boto3
import pandas as pd
from io import StringIO, BytesIO
from datetime import datetime, timedelta

class Extract:
    def __init__(self):
        # Parameters/Configurations
        self.arg_date = '2022-03-02'
        self.src_format = '%Y-%m-%d'
        self.src_bucket = 'deutsche-boerse-xetra-pds'
        self.trg_bucket = 'xetra-bucket-2022-03-02-gerardo'
        self.columns = ['ISIN', 'Date', 'Time', 'StartPrice', 'MaxPrice', 'MinPrice', 'EndPrice', 'TradedVolume']
        self.key = 'xetra_daily_report_' + datetime.today().strftime("%Y%m%d_%H%M%S") + '.parquet'
        # Init    
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(self.src_bucket)
        self.objects = return_objects(self.src_bucket, self.src_format,self.arg_date, self.bucket)
        df_all = extract(self.objects, self.bucket, self.columns, self.key)
        df_all =  self.transform_report(df_all, self.arg_date, self.columns)
        self.bucket_target = write_df_to_s3(self.trg_bucket, self.key, df_all, self.s3)

def read_csv_to_df(filename, bucket):
    csv_obj = bucket.Object(key=filename).get().get('Body').read().decode('utf-8')
    data = StringIO(csv_obj)
    df = pd.read_csv(data, delimiter=',')
    return df

def write_df_to_s3(self, df_all, s3):
    out_buffer = BytesIO()
    df_all.to_parquet(out_buffer, index=False)
    bucket_target = s3.Bucket(self.trg_bucket)
    bucket_target.put_object(Body=out_buffer.getvalue(), Key=self.key)
    return bucket_target

def return_objects(self, bucket):
    self.arg_date_dt = datetime.strptime(self.arg_date, self.src_format).date() - timedelta(days=1)
    objects = [obj for obj in bucket.objects.all() if datetime.strptime(obj.key.split('/')[0], self.src_format).date() >= self.arg_date_dt]
    ##objKey= obj.key
    return objects

def extract(self, objects, bucket):
    df_all = pd.concat([read_csv_to_df(obj.self.key, bucket) for obj in objects], ignore_index=True)
    df_all = df_all.loc[:, self.columns]
    df_all.dropna(inplace=True)
    return df_all

