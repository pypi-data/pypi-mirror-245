# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
import boto3
from botocore.config import Config

from .utils import get_setting

A = lambda c: get_setting('S3', c)
SECRET_ID = A('SECRET_ID')
SECRET_KEY = A('SECRET_KEY')
REGION = A('REGION') or "us-west-2"
BUCKET = A('BUCKET')


def gen_signature(key, secret_id=SECRET_ID, secret_key=SECRET_KEY, expire=300,
                  bucket=BUCKET, method='put', region=REGION, **kwargs):
    s3 = boto3.client('s3',
                      aws_access_key_id=secret_id,
                      aws_secret_access_key=secret_key,
                      config=Config(signature_version='s3v4'),
                      region_name=region)
    params = dict(
        Bucket=bucket,
        Key=key,
        **kwargs
    )
    url = s3.generate_presigned_url(
        '%s_object' % method,
        Params=params,
        ExpiresIn=expire
    )
    return dict(bucket=bucket, region=REGION, url=url)


def down_and_upload_to_aws(url, bucket=BUCKET, cloudfront_domain=None):
    import boto3, hashlib
    from xyz_util.crawlutils import http_get
    from django.core.files.base import ContentFile
    s3 = boto3.client('s3')
    r = http_get(url)
    md5 = hashlib.md5()
    fd = r.content
    md5.update(fd)
    ct = r.headers['Content-Type']
    ps = ct.split('/')
    fpath = 'resource/%s/%s.%s' % (ps[0], md5.hexdigest(), ps[1])
    import requests
    r = requests.put(url, data=ContentFile(fd))
    if r.status_code != 200:
        raise Exception("Error(%s): %s" % (r.status_code, r.text))
    # s3.upload_fileobj(ContentFile(fd), bucket, fpath, ExtraArgs=dict(ACL='public-read', ContentType=ct))
    domain = cloudfront_domain if cloudfront_domain else '%s.s3.%s.amazonaws.com' % (bucket, s3.meta.region_name)
    return 'https://%s/%s' % (domain, fpath)
