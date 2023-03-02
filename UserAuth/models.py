from django.db import models

# Create your models here.

class Web3User(models.Model):
    # 字段 用户名 头像URL 地址 Nonce
    username = models.CharField(max_length=20)
    avatar = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    nonce = models.IntegerField()