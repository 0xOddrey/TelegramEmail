from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.views.generic import TemplateView
from django.core import mail
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import _datetime
from datetime import datetime
from decouple import config, Csv
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from celery import shared_task
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config, Csv 
import requests
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
# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")

app = Celery("base")


       

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)