from django.db import models
import requests
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.files.base import ContentFile
import os

# Create your models here.
class Coin(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    precision = models.PositiveSmallIntegerField()
    _type = models.CharField(max_length=50)

    def __str__(self):
        return self.code
    
@receiver(post_migrate)
def populate_currency(sender, **kwargs):
    url = "https://bisq.markets/api/currencies"
    # faz a solicitação HTTP
    response = requests.get(url)
    # extrai o valor do Bitcoin em relação ao dólar americano a partir dos dados JSON
    json_dict = response.json()
    # verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        for key, value in json_dict.items():
            Coin.objects.create(code=value['code'], name=value['name'], precision=value['precision'], _type=value['_type'])