from django.conf.urls import url
import tgbot.views

urlpatterns = [
    url(r'^webhook/123$', tgbot.views.webhook, name='webhook'),
]
'''
#insert csv file 

import logging
from os import path
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Count
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from telegram.error import BadRequest
from telegram.error import Unauthorized

from deep.constants import *
from tgbot.models import Record, Text, People
import pandas as pd
import pandas as pd
your_dataframe = pd.read_csv('normal.csv')
li=['هیچ جۆرە دەرمانێک بۆ ئەو نەخۆشییە نەبوو']
# dellete all data in table
Text.objects.all().delete()

for line,vile in zip(your_dataframe.values,your_dataframe.index):
    x='000%s'%vile
    Text.objects.create(text=line[0], phonetic="qewe", code=x,
                                      sample_voice="sample_voices/2_Y4dRbRy.wav")
'''