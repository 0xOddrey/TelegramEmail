try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from django.conf import settings
if getattr(settings, 'POSTMAN_I18N_URLS', False):
    from django.utils.translation import pgettext_lazy
else:
    def pgettext_lazy(c, m): return m

from django.urls import path, include, re_path
from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .views import *


urlpatterns = [

    url(r'^$',
        view=Homepage, 
        name='homepage'),

    url(r'confirmation/',
        view=Confirmation, 
        name='confirmation'),

    url('add-message/',
        view=AddMessage, 
        name='add_message'),


]