import requests
import xmltodict
import sys
import os
from celery import Celery
from celery.utils.log import get_task_logger
import asyncio


sys.path.append(os.getcwd())
from models.accounttype import accounttypes_table
from models.database import database


celery = Celery('testcelery', broker='amqp://user:bitnami@rabbitmq:5672//')
celery.autodiscover_tasks()
celery_log = get_task_logger(__name__)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):    
    # update currency every 6000 sec
    sender.add_periodic_task(6000.0, check_currency, expires=10)


async def insert_values(query, values):
    await database.execute_many(query=query, values=values)
    query2 = accounttypes_table.select().where(accounttypes_table.c.currency == "USD")
    print(await database.fetch_one(query2))


@celery.task
def check_currency():
    full_page = requests.get("https://www.cbr-xml-daily.ru/daily.xml")
    data = xmltodict.parse(full_page.content)
    usd = str(data['ValCurs']['Valute'][10]['Value']).replace(',','.')
    euro = str(data['ValCurs']['Valute'][11]['Value']).replace(',','.')
    query = accounttypes_table.insert()
    values = [
        {"currency": "RUB", "value": float(1)},
        {"currency": "USD", "value": float(usd)},
        {"currency": "EURO", "value": float(euro)},
    ]
    asyncio.run(insert_values(query, values))
    

