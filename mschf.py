import requests
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
import time 
import json 
import urllib.parse

session = requests.Session()

captchatoken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXRhZGF0YSI6eyJjaGVja291dFNlc3Npb25JZCI6ImRhMjYxN2E0LTYzY2UtNGFiNC05NDI1LWIyZDQxNjE1ZDE4ZiIsImNhcnRJZCI6IjE0ZGYyMTc2LWZmY2UtNDU4Yy05ZmYwLTNhOWU3M2JjZjY0NyJ9LCJyb2xlIjoiZ3Vlc3QiLCJzY29wZSI6ImNoZWNrb3V0Iiwic3ViIjp7InVzZXJJZCI6ImI5MWUwYTdjLWE4NWEtNDZlYS04N2JiLWFlNDdjY2I5NzA2OCJ9LCJpYXQiOjE2NzY0OTc2MzMsImV4cCI6MTY3NzEwMjQzM30.s1z1xkYgTQOHbqBQXGLtAmsucGB48X6HXdtJ7wj5ld0'
expmonth = '05'
expyear = '26'
zipcode = '83644'
cvv = '416'
cardnumber1 = '5462 9116 7890 1909'
cardnumber = urllib.parse.quote(cardnumber1)
print(cardnumber)

selectedsize = input('SELECT SIZE:')
selected_size = "Size " + str(selectedsize)
quantity = input('SELECT QUANTITY:')
dropid = input('ENTER DROP ID (CAN BE FOUND IN DISC, IF NEWEST RELEASE PUT NEW/NEWEST):')
if dropid.lower() in ['new', 'newest']:
    dropid = 'bigredboot'
else:
    dropid = dropid.lower()
    print(dropid)
    
    
def productids():
    url = 'https://gw.prod.api.mschf.xyz/sneakers/v2'
    
    headers = {
        'Host': 'gw.prod.api.mschf.xyz',
        'Accept': '/',
        'User-Agent': 'Sneakers/39 CFNetwork/1335.0.3 Darwin/21.6.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }
    
    response = requests.get(url, headers=headers)
    
    data = response.json()
    
    for product in data:
        print(product)
        if product['publicId'] == dropid:
            uuids = product["productVariants"]

    for size in uuids:
        if selectedsize == size['size']:
            value = size['id']
    
    return value      
value = productids()
def checkoutsession(value, quantity, dropid, captchatoken):
    url = "https://gw.prod.api.mschf.xyz/checkout-sessions"


    payload = {
        "_type": "direct",
        "workflow": "patch_all",
        "version": "1.0.2",
        "dropId": dropid,
        "lineItems": [
            {
                "type": "item",
                "productId": value,
                "quantity": 1
            }
        ],
        "intent": "payment",
        "shippingDetails": {"address": {"country": "US"}}
    }
    headers = {
        "authority": "gw.prod.api.mschf.xyz",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": captchatoken,
        "content-type": "application/json",
        "origin": "https://checkout.mschf.com",
        "referer": "https://checkout.mschf.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = session.post(url, json=payload, headers=headers)

    print(response.status_code)
    response_dict = response.json()  # Convert response to Python dictionary

    id = response_dict['id']  # Access the 'id' value from the dictionary
    
    print('GOING TO CHECKOUT...')
    
    return id
id = checkoutsession(value, quantity, dropid, captchatoken)

def continuecheckout(value, quantity, dropid, id, captchatoken):
    url = "https://gw.prod.api.mschf.xyz/checkout-sessions/"+id

    payload = {
        "_type": "direct",
        "workflow": "patch_all",
        "version": "1.0.2",
        "dropId": dropid,
        "lineItems": [
            {
                "type": "item",
                "productId": value,
                "quantity": quantity
            }
        ],
        "intent": "payment",
        "shippingDetails": {
            "phone": "+12085509662",
            "email": "skysnkrs@gmail.com",
            "name": "Tristan Sky_Snkrs",
            "address": {
                "country": "US",
                "line1": "1910 Ridge Way",
                "city": "MIDDLETON",
                "postalCode": "83644",
                "state": "ID"
            }
        }
    }
    headers = {
        "authority": "gw.prod.api.mschf.xyz",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": captchatoken,
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = session.patch(url, json=payload, headers=headers)
    
    response_dict = response.json()  # Convert response to Python dictionary

    paymentid = response_dict['paymentIntentId']
    clientsecret = response_dict['clientSecret']
    publishablekey = response_dict['publishableKey']
    
    print('SUBMITTING INFO...')
    return paymentid, clientsecret, publishablekey
paymentid, clientsecret, publishablekey = continuecheckout(value, quantity, dropid, id, captchatoken)

def startpayment(paymentid, clientsecret, publishablekey):
    url = "https://api.stripe.com/v1/elements/sessions"

    querystring = {"key":publishablekey,"type":"order","locale":"en-US","client_secret":clientsecret}

    headers = {
        "authority": "api.stripe.com",
        "accept": "application/json",
        "Stripe-Version":"2022-08-01; orders_beta=v4",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = session.get(url, headers=headers, params=querystring)

    print('STARTING PAYMENT...')
    
startpayment(paymentid, clientsecret, publishablekey)

def paymentsubmit(paymentid, clientsecret, publishablekey):
    url = "https://api.stripe.com/v1/orders/"+paymentid+"/submit"

    payload = "key="+publishablekey+"&client_secret="+clientsecret+"&expand%5B0%5D=payment.payment_intent"
    headers = {
        "authority": "api.stripe.com",
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Stripe-Version": "2022-08-01; orders_beta=v4"
    }

    response = session.post(url, data=payload, headers=headers)


    
    response_dict = response.json()  # Convert response to Python dictionary

    id2 = response_dict['payment']['payment_intent']['id']
    clientsecretupdated = response_dict['payment']['payment_intent']['client_secret']
    
    
    print('PAYMENT PROCESSING...')
    return id2, clientsecretupdated

id2, clientsecretupdated = paymentsubmit(paymentid, clientsecret, publishablekey)

def confirmorder(id2, clientsecretupdated, paymentid, clientsecret, captchatoken, publishablekey, id, cvv, cardnumber, zipcode, expyear, expmonth):
    
    
    url = "https://api.stripe.com/v1/payment_intents/"+id2+"/confirm"

    payload = payload = "return_url=https%3A%2F%2Fcheckout.mschf.com%2F%23%2Fconfirmation%2F"+id+"%3FcsToken%"+captchatoken+"&payment_method_data%5Btype%5D=card&payment_method_data%5Bcard%5D%5Bnumber%5D="+cardnumber+"&payment_method_data%5Bcard%5D%5Bcvc%5D=670&payment_method_data%5Bcard%5D%5Bexp_year%5D="+expyear+"&payment_method_data%5Bcard%5D%5Bexp_month%5D="+expmonth+"&payment_method_data%5Bbilling_details%5D%5Baddress%5D%5Bpostal_code%5D="+zipcode+"&payment_method_data%5Bbilling_details%5D%5Baddress%5D%5Bcountry%5D=US&payment_method_data%5Bpasted_fields%5D=number&expected_payment_method_type=card&use_stripe_sdk=true&key="+publishablekey+"&client_secret="+clientsecretupdated
    print(payload)
    input()
    headers = {
        "authority": "api.stripe.com",
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Stripe-Version": "2022-08-01; orders_beta=v4"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    response_dict = response.json()  # Convert response to Python dictionary

    print(response_dict)
    
confirmorder(id2, clientsecretupdated, paymentid, clientsecret, captchatoken, publishablekey, id, cvv, cardnumber, zipcode, expyear, expmonth)