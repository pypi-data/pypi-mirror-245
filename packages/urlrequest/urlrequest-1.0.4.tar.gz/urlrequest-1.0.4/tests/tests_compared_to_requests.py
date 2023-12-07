import requests
from urlrequest import UrlRequest

def compare(urlr,req):
    try:
        assert urlr.text == req.text
    except:
        print("------- urlrequest ------")
        print(urlr.text)
        print("========================")
        print("")
        print("------- requests ------")
        print(req.text)
        print("========================")
    try:
        assert urlr.json() == req.json()
    except:
        print("------- urlrequest ------")
        print(urlr.json())
        print("========================")
        print("")
        print("------- requests ------")
        print(req.json())
        print("========================")
    try:
        assert urlr.status_code == req.status_code
    except:
        print("------- urlrequest ------")
        print(urlr.status_code)
        print("========================")
        print("")
        print("------- requests ------")
        print(req.status_code)
        print("========================")
    

#get test
urlr =  UrlRequest.get("https://httpbin.org/ip")
req =   requests.get("https://httpbin.org/ip")
compare(urlr,req)

#auth test
urlr =  UrlRequest.get("https://httpbin.org/basic-auth/user/password",auth=('user','password'))
req =   requests.get("https://httpbin.org/basic-auth/user/password",auth=('user','password'))
compare(urlr,req)

#post test
urlr =  UrlRequest.post("https://httpbin.org/response-headers",data={'test':33234})
req =   requests.post("https://httpbin.org/response-headers",data={'test':33234})
compare(urlr,req)
