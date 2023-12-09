from django.db import models


class GameCreatorAuth(models.Model):
    "登录"

    id = models.AutoField(primary_key=True)
    "唯一标识符"

    uid = models.CharField(max_length=255)
    "uid"

    username = models.CharField(max_length=255)
    "名称"

    auth_token = models.CharField(max_length=255)
    "重新生成的唯一标识符"

    updated_at = models.DateTimeField()
    "更新日期"

    class Meta:
        app_label = "gamecreator_auth"
