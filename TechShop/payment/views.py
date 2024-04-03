import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order


# instantiate Braintree payment gateway

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        nonce =request.POST.get('payment_method_nonce', None) # retrieve the nonce
        result = gateway.transaction.sale ({'amount': f'{total_cost: .2f}', 
        'payment_method_nonce':nonce, 'options':{submit_for_settlement: True}}) # creates abd submits the transaction

        if result.is_success:
            order.paid = True # mark the order is paid
            order.braintree_id = result.transaction.id #stores the unique transaction id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment: canceled')
    
    else:
        client_token = gateway.client_token.generate() # To generate client token
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})




def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')















""""Let's create a view for processing payments. The whole checkout process will work
as follows:
1. In the view, a client token is generated using the braintree Python module.
This token is used in the next step to instantiate the Braintree JavaScript
client; it's not the payment token nonce.
2. The view renders the checkout template. The template loads the Braintree
JavaScript SDK using the client token and generates the iframe with the
hosted payment form fields.
3. Users enter their credit card details and submit the form. A payment token
nonce is generated with the Braintree JavaScript client. You send the token
to your view with a POST request."""

"""4. The payment view receives the token nonce and you use it to generate a transaction using the braintree Python module."""



#Mpesa Payment Integration

from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . credentials import MpesaAccessToken, LipanaMpesaPpassword


def getAccessToken(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254707535013,
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254707535013,
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Alex",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')
'''
def pull_transaction(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "EndDate": LipanaMpesaPpassword.EndDate,
        "OffSetValue": "0"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')
'''