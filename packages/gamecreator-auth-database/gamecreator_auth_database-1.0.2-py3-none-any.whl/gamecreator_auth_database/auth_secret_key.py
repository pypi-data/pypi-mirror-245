from django.db import models


class AuthSecretKey(models.Model):
    "密钥管理"

    id = models.AutoField(primary_key=True)
    "唯一标识符"

    type = models.CharField(max_length=255)
    "类型"

    secret_key = models.CharField(max_length=255)
    "密钥"

    class Meta:
        app_label = "auth_secret_key"
