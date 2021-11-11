import requests
import xmltodict
from models.accounttype import accounttypes_table
from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"
celery.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'check_currency',
        'schedule': 30.0
    },
}

@celery.task(name="check_currency")
def check_currency():
    full_page = requests.get("https://www.cbr-xml-daily.ru/daily.xml")
    data = xmltodict.parse(full_page.content)
    usd = data['ValCurs']['Valute'][10]['Value']
    euro = data['ValCurs']['Valute'][11]['Value']
    print(usd, euro)