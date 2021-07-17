from django.core.mail import EmailMultiAlternatives
from background_task import background
from tinakala.settings import EMAIL_HOST_USER


@background(schedule=5)
def admin_sent_news_mail(subject, content, html, users):
    mail = EmailMultiAlternatives(subject, content, EMAIL_HOST_USER, users)
    mail.attach_alternative(html, 'text/html')
    mail.send()
