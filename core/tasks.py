from celery import shared_task
from time import sleep
from django.core.mail import send_mail


# @shared_task
# def add(x, y, id):
#     sleep(7)
#     num = Number.objects.get(id=id)
#     num.result = x + y
#     num.save()
#     return num.result


@shared_task
def show():
    send_mail('Celery', 'Hello World', 'shayan.aimoradii@gmail.com', ['redbull.9248@gmail.com'])
