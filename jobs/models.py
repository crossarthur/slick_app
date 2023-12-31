from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from twilio.base.exceptions import TwilioException
from twilio.rest import Client
from dotenv import load_dotenv
import os
# Create your models here.


class Prints(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Jobs(models.Model):
    customer_name = models.CharField(max_length=50)
    print = models.ForeignKey(Prints, on_delete=models.CASCADE, related_name='prints')
    height = models.FloatField()
    width = models.FloatField()
    unit_price = models.FloatField(default=0, null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    total_height = models.FloatField(null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


@receiver(pre_save, sender=Jobs)
def set_balance(sender, instance, *args, **kwargs):

    if instance.cost is None:
        instance.cost = int(instance.height * instance.width * instance.unit_price)
    else:
        pass


class CloseRecord(models.Model):
    name_record = models.CharField(max_length=30)
    total_jobs = models.CharField(max_length=20)
    total_sav = models.CharField(max_length=20, null=True, blank=True)
    total_flex = models.CharField(max_length=20, null=True, blank=True)
    total_cost = models.CharField(max_length=20, null=True, blank=True)
    close_account = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_record

load_dotenv()

class Contact(models.Model):
    name = models.CharField(max_length=40)
    phone_number = models.PositiveIntegerField()
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            account_sid = os.getenv('account_sid')
            auth_token = os.getenv("auth_token")

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                         body=f"You have received a message from {self.name} in SlICK-TS App",
                         from_='+16626671874',
                         to='+2348033248599'
                     )

            print(message.sid)
        except TwilioException:
            return super().save(*args, **kwargs)
