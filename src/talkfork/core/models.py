from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


class User(AbstractUser):

    oauth2_code = models.CharField(max_length=100)


# token = Token.objects.create(user=models.ForeignKey(AbstractUser))
# print(token.key)
