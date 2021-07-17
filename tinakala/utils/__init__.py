from tinakala.utils.permission_decorator import *
from tinakala.utils.upload_file_manager import *
from tinakala.utils.otp_sender import *
from tinakala.utils.slug_generator import *
from tinakala.utils.grouper import *
from tinakala.utils.product_methods import *
from tinakala.utils.get_client_ip import *
from tinakala.utils.send_mail import *
from tinakala.utils.cron_job_process import *


def percent_2_text(percent):
    if 0 <= percent <= 20:
        return 'بد'
    if 20 < percent <= 40:
        return 'ضعیف'
    if 40 < percent <= 60:
        return 'متوسط'
    if 60 < percent <= 80:
        return 'خوب'
    if 80 < percent <= 100:
        return 'عالی'


def check_vote(expr):
    if expr is not None:
        return expr
    else:
        return 0
