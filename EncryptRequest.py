#!/usr/bin/python3.4
from urllib.request import Request, urlopen
import base64

if __name__ == "__main__":
   try:
       
       message = b'YES'
       
       encode = base64.b64encode(message) 
       decode = base64.b64decode(encode)
       print(encode)
       url='http://www.google.com'
       req = Request(url)
       req.add_header('TEST', encode.decode('utf-8'))
       resp = urlopen(req).read()
       #print(resp)
   except:
       raise
