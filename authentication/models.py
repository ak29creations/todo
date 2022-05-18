from django.db import models
from django.contrib.auth.models import User


class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_added = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(max_length=6)
