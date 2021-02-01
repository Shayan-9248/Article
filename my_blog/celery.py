from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')

app = Celery('my_blog')
app.autodiscover_tasks()

app.conf.broker_url = 'amqp://localhost'
app.conf.result_backend = 'rpc://'
app.conf.result_serializer = 'json'
app.conf.result_expires = timedelta(days=1)
