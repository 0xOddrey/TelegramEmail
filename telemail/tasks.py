
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from base.celery import app
from django.views.generic import TemplateView
from django.core import mail
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import _datetime
from datetime import datetime
from .models import *
from decouple import config, Csv
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from celery import shared_task
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from decouple import config, Csv
from django.template.loader import get_template

import requests
from base.celery import app

from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon import TelegramClient, events, sync
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
import asyncio
import json
import logging
logging.basicConfig(level=logging.DEBUG)
from base.celery import app


# Setting configuration values
api_id = config("api_id")
api_hash = config("api_hash")

api_hash = str(api_hash)

phone = config("phone")
username = config("username")

SESSION = os.environ.get('TG_SESSION', 'quart')

@app.task
def runTelethon(arg):
    print(arg)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(SESSION,api_id,api_hash, loop=loop).start()
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        me = client.sign_in(phone, input('Enter code: '))

    channel_entity = client.get_entity(PeerChannel(int(config('PEER_CHANNEL'))))

    offset_id = 0
    limit = 20
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        history = client(GetHistoryRequest(
            peer=channel_entity,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            if message.pinned:
                result = message.to_dict()
                t_messages = {"id":result["id"], "message":result["message"]}
                all_messages.append(t_messages)
                
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    
    api_url = "http://telemail.herokuapp.com/add-message/"
    requests.post(api_url, json=all_messages)
    print(api_url)
    client.disconnect() 

@app.on_after_finalize.connect
def app_ready(**kwargs):
    """
    Called once after app has been finalized.
    """
    sender = kwargs.get('sender')

    # periodic tasks
    speed = 60
    sender.add_periodic_task(speed, runTelethon.s('starting message pull'),name='update leases every {} seconds'.format(speed))



def send_pinned_email():
    all_users = telegram_user.objects.all()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    
    allMessages = pinnedMessage.objects.filter(timestamp__range=[start_date, end_date], is_sent=False)

    for user in all_users:
        user_email = user.email
        message = Mail(
            from_email='audrey@nanupanda.com',
            to_emails=user_email ,
            subject='CPG Club',
            html_content=get_template('summary_email.html').render({'allMessages': allMessages}))
        try:
            sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            pass

