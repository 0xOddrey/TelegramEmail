from django.db import models
from datetime import datetime 


class telegram_user(models.Model):
    email = models.EmailField(blank=True,
                              null=True)       
    wallet = models.CharField(max_length=200)    
    timestamp = models.DateTimeField(blank=True,
                               null=True)

    def __str__(self):
        return "%s" % (self.email)



class pinnedMessage(models.Model):
    timestamp = models.DateTimeField(blank=True,
                               null=True)
    message = models.CharField(max_length=1500)
    pmesssage = models.IntegerField(default = 0,
                               blank=True,
                               null=True)
    is_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.utcnow()
        return super(pinnedMessage, self).save(*args, **kwargs)

    def __str__(self):
        return "%s: %s" % (self.pmesssage, self.timestamp)