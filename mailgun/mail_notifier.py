import datetime
import os
import requests

from database import ad_dao

mailgun_url = os.getenv("MAILGUN_URL")
api_key = os.getenv("API_KEY")
mail = os.getenv("MAIL")


def notify():
    ads = get_ads()


def get_ads():
    min_date = datetime.datetime(2014, 1, 1, 0, 0, 0)
    return ad_dao.retrieve({
        "$and:": [
            {"Queue": {"$elemMatch": {"$lt": min_date}}},
            {"Type": {"$nin": ["Student"]}}
        ]
    })


def mailgun(recipient, message):
    requests.post(mailgun_url, auth=("api", api_key), data={
        'from': 'bf-notifier@torbacka.se',
        'to': recipient,
        'subject': 'Intressa lägenheter från (bostad.stockholm.se)',
        'text': message
    })
