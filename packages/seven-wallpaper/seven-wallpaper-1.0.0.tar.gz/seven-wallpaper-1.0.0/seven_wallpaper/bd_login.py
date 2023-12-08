
import hashlib
import hmac
import string
import datetime
import requests
import json
import time

AUTHORIZATION = "authorization"
BCE_PREFIX = "x-bce-"
DEFAULT_ENCODING = 'UTF-8'

# 根据RFC 3986，除了：
#   1.大小写英文字符
#   2.阿拉伯数字
#   3.点'.'、波浪线'~'、减号'-'以及下划线'_'
# 以外都要编码
RESERVED_CHAR_SET = set(string.ascii_letters + string.digits + '.~-_')

def get_normalized_char(i):
    char = chr(i)
    if char in RESERVED_CHAR_SET:
            return char
    else:
        return '%%%02X' % i
NORMALIZED_CHAR_LIST = [get_normalized_char(i) for i in range(256)]

# 正规化字符串
def normalize_string(in_str, encoding_slash=True):
    if in_str is None:
        return ''

    def is_reverse_char(c):
        return not ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9')
            or c == '-' or c == '_' or c == '.' or c == '~')

    def byte_to_hex(b):
        return format(b, 'X').zfill(2)

    result = []
    for item in in_str.encode('utf-8'):
        c = chr(item)
        if is_reverse_char(c) and c != '/':
            result.append('%' + byte_to_hex(item))
        else:
            result.append(c)
    return ''.join(result)


# 生成规范时间戳
def get_canonical_time(timestamp=0):
    # 不使用任何参数调用的时候返回当前时间
    if timestamp == 0:
        utctime = datetime.datetime.utcnow()
    else:
        utctime = datetime.datetime.utcfromtimestamp(timestamp)

    # 时间戳格式：[year]-[month]-[day]T[hour]:[minute]:[second]Z
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (
        utctime.year, utctime.month, utctime.day,
        utctime.hour, utctime.minute, utctime.second)


# 生成规范URI
def get_canonical_uri(path):
    # 规范化URI的格式为：/{bucket}/{object}，并且要对除了斜杠"/"之外的所有字符编码
    return normalize_string(path, False)


# 生成规范query string
def get_canonical_querystring(params):
    if params is None:
        return ''

    # 除了authorization之外，所有的query string全部加入编码
    result = ['%s=%s' % (k, normalize_string(v)) for k, v in params.items() if
              k.lower != AUTHORIZATION]

    # 按字典序排序
    result.sort()

    # 使用&符号连接所有字符串并返回
    return '&'.join(result)


# 生成规范header
def get_canonical_headers(headers, headers_to_sign=None):
    headers = headers or {}

    # 没有指定header_to_sign的情况下，默认使用：
    #   1.host
    #   2.content-md5
    #   3.content-length
    #   4.content-type
    #   5.所有以x-bce-开头的header项
    # 生成规范header
    if headers_to_sign is None or len(headers_to_sign) == 0:
        headers_to_sign = {"host", "content-md5", "content-length", "content-type"}

    # 对于header中的key，去掉前后的空白之后需要转化为小写
    # 对于header中的value，转化为str之后去掉前后的空白
    f = lambda key, value: (key.strip().lower(), str(value).strip())

    result = []
    '''head_list= list(headers.items())
    heads= map(f, head_list)'''
    for k, v in headers.items():
        # 无论何种情况，以x-bce-开头的header项都需要被添加到规范header中
        if k.startswith(BCE_PREFIX) or k in headers_to_sign:
            result.append("%s:%s" % (normalize_string(k.strip().lower()), normalize_string(v.strip())))

    # 按照字典序排序
    #result.sort()

    # 使用\n符号连接所有字符串并返回
    return '\n'.join(result)


# 签名主算法
def sign(credentials, http_method, path, headers, params,
         timestamp=0, expiration_in_seconds=18000, headers_to_sign=None):
    headers = headers or {}
    params = params or {}

    # 1.生成sign key
    # 1.1.生成auth-string，格式为：bce-auth-v1/{accessKeyId}/{timestamp}/{expirationPeriodInSeconds}
    sign_key_info = 'bce-auth-v1/%s/%s/%d' % (
        credentials.access_key_id,
        get_canonical_time(timestamp),
        expiration_in_seconds)
    # 1.2.使用auth-string加上SK，用SHA-256生成sign key
    sign_key = hmac.new(
        credentials.secret_access_key.encode("utf-8"),
        sign_key_info.encode("utf-8"),
        hashlib.sha256).hexdigest()

    # 2.生成规范化uri
    canonical_uri = get_canonical_uri(path)

    # 3.生成规范化query string
    canonical_querystring = get_canonical_querystring(params)

    # 4.生成规范化header
    canonical_headers = get_canonical_headers(headers, headers_to_sign)
    # 5.使用'\n'将HTTP METHOD和2、3、4中的结果连接起来，成为一个大字符串
    string_to_sign = '\n'.join(
        [http_method, canonical_uri, canonical_querystring, canonical_headers])

    # 6.使用5中生成的签名串和1中生成的sign key，用SHA-256算法生成签名结果
    sign_result = hmac.new(sign_key.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # 7.拼接最终签名结果串
    if headers_to_sign:
        # 指定header to sign
        result = '%s/%s/%s' % (sign_key_info, ';'.join(headers_to_sign), sign_result)
    else:
        # 不指定header to sign情况下的默认签名结果串，但百度智能云API的唯一要求是Host域必须被编码，所以此处需要至少添加上host
        result = '%s/host/%s' % (sign_key_info, sign_result)  # 官网demo需要改的地方
    return result


class BceCredentials(object):
    def __init__(self,access_key_id = "3317cf489b1c4f16a9b4549810441870",secret_access_key = "361230f0464d4830b6daef0a8f56c877"):
        self.access_key_id =access_key_id        
        self.secret_access_key = secret_access_key

class BDLoginHelper():
    staticmethod
    def get_code(token):
        # 填写AK SK
        credentials = BceCredentials()  # 填写ak、sk
        # API接口的请求方法
        http_method = "GET"
        # 接口请求路径
        path = "/v1/token2phone"
        # 接口请求的header头
        timestamp = int(time.time())
        headers = {
            "host": "pnvs.baidubce.com",
            "content-type": "application/json; charset=utf-8",
            "x-bce-date": get_canonical_time(timestamp),
        }
        # 接口请求参数
        params = {
            "token": token,
        }
        # 接口请求的body数据
        body = {
        }
        # 设置参与鉴权编码的header，即headers_to_sign,至少包含host，百度智能云API的唯一要求是Host域必须被编码
        headers_to_sign = {
            "x-bce-date",
            "host",            
        }
        # 设置到期时间，默认1800s
        expiration_in_seconds = 18000
        # 设置参与鉴权的时间戳
        #timestamp = int(time.time())
        # 生成鉴权字符串
        result = sign(credentials, http_method, path, headers, params, timestamp, expiration_in_seconds,
                    headers_to_sign)
        # 使用request进行请求接口
        request = {
            'method': http_method,
            'uri': path,
            'headers': headers,
            'params': params
        }
        # headers字典中需要加上鉴权字符串authorization的请求头
        headers['authorization'] = result

        # 拼接接口的url地址
        url = 'https://%s%s?token=%s' % (headers['host'], request['uri'], params['token'])
        # 发起请求
        response = requests.request(request["method"], url, headers=headers, data=json.dumps(body))
        if response.status_code==200:
            result_dict=json.loads(response.text)
            return result_dict
        else:
            return response.status_code
    

if __name__=="__main__":
    token='''goxuoy3I4ZB2kXjSO6MvCGtez_CKXP8h2xjtk9t2PHgrkqrlIPXUX9WO7m25gK-YfIODgCmM1-w2yC3QCGaxdW52nXe7MvykXoy3CqzTVLeN670F2dKIshEJJv35ixSe-5NZtAli0Mthf7wRCtLAdx8WphBlPK7ZcJXQfWGE71W6MnqndkePKBpoSNqOyeUmnnQydqegtfk1iOinYrVQrk5FV2l9qlsDNncABVGp4VYIc2gPdEq7PKUd72NiheAGvAOiG43Zm4tv5AX_-kTLfOW3k6ZLtyLcQwaKJd9DAFyJI-3yrddmsC8ey1qUPemavR4ox4l0DqF4AYuqLvf5NBAdJVJGaaoXw6FkuUx3Io29p_OYBFzu8X3QXnyu6Y58CVwwAMejWdRNRJ0M_IipTXtgJNjz871dmVUptAgOoc_1ZOGyVLm-J_DGuc5irQxicDoSc9x8OezbiCVy6lj5Rhb6UItapK_3sosGWrjfW_05wMCsuOLvtUbKkZXjtcRPKXtcz78gZiupO9ylSvxvHM_94vr8BUn4iHHk0D9MLibgy1_pu-xV1hMFLC4xF4bdzK4j_Wgf7caM0uBjhGfperphU2WJ0_Jw-0Fe5hHG0xw'''
    print(BDLoginHelper.get_code(token))

    