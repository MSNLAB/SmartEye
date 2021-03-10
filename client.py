from urllib import request, parse
import base64


url = 'http://127.0.0.1:5000/hello'
headers = {
    # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    # 'Host': 'httpbin.org'
}
with open('weixin_20210310133657.png', 'rb') as f:
    img_byte = base64.b64encode(f.read())  # 二进制读取后变base64编码
    img_str = img_byte.decode('ascii')
dict = {
    'name': 'Germey',
    'image': img_str
}
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, data=data, headers=headers, method='POST')

response = request.urlopen(req)

img = response.read().decode('utf-8')
img_decode_ = img.encode('ascii')
img_decode = base64.b64decode(img_decode_)
with open('meelo.jpg', 'wb') as f:
    f.write(img_decode)