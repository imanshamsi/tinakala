from random import randint
from kavenegar import *
from tinakala.settings import KAVENEGAR_KEY


def get_random_otp():
    return randint(10000, 99999)


def send_otp(mobile, otp, message):
    mobile = [mobile, ]
    try:
        api = KavenegarAPI(KAVENEGAR_KEY)
        params = {
            'sender': '1000596446',
            'receptor': mobile,  # multiple mobile number, split by comma
            'message': f'{message} : {otp}',
        }
        response = api.sms_send(params)
        # print(otp)
        # print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
