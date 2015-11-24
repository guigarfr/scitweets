#coding: utf8

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from tweets.models import Tweet
import json
from datetime import datetime
import os


class Command(BaseCommand):
    help = 'Imports data'

    TW_DIR = 'tweets/data'
    TW_IMPORTED = 'imported'

    def handle(self, *args, **options):
        for f in os.listdir(self.TW_DIR):
            if f.endswith('.json'):
                with open(os.path.join(self.TW_DIR, f)) as data_file:    
                    data = json.load(data_file)

                for d in data:
                    tweet_text = unicode(d['text'])
                    q, _ = Tweet.objects.get_or_create(id_twitter=int(d['id']), text=tweet_text)

                    print "Created tweet with id", q.pk, q.id_tweeter
                    # q.save()

                prefix = str(int((datetime.now() - datetime(1970, 1, 1)).total_seconds())) + '_'
                os.rename(os.path.join(self.TW_DIR, f), os.path.join(self.TW_DIR, self.TW_IMPORTED, prefix + f))
