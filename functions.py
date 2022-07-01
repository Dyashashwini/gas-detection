import urequests
import network
from time import sleep
import ujson
import ubinascii

def connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print(".",end="")
            sleep(1)
    print('network config:', sta_if.ifconfig())

def sms(body):
    # Variables
    error = False
    account_sid = "AC28e303c4*******************"
    auth_token = "02feaea28af*******************"
    from_ = "+1712430*****"
    to = ["+91798972****", "+91798101****"]
    twilio_auth = ubinascii.b2a_base64('{sid}:{token}'.format(sid=account_sid, token=auth_token)).strip()
    url = 'https://api.twilio.com/2010-04-01/Accounts/'+ account_sid +'/Messages.json'
    # Making a POST Request to the url with data
    for num in to:
        data = 'Body={}&From={}&To={}'.format(body, from_, num)
        r = urequests.post(
            url,
            data=data,
            headers={
                'Authorization': b'Basic ' + twilio_auth,
                'Content-Type': 'application/x-www-form-urlencoded'
                }
            ).json()
        if r['error_code'] != None:
            error = True
    return False if error else True
