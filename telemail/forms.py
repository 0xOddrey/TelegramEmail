from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import inlineformset_factory, BaseModelFormSet
from django.forms import ModelChoiceField, RadioSelect
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from .models import *
import datetime
from datetime import datetime

class telegram_userForm(forms.ModelForm):

    class Meta:
        model = telegram_user
        fields = '__all__'