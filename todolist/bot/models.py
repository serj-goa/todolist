from django.db import models as m

from core.models import CustomUser


class TgUser(m.Model):
    chat_id = m.BigIntegerField(verbose_name='Идентификатор чата', unique=True)
    username = m.CharField(verbose_name='Имя пользователя', max_length=255, null=True, blank=True, default=None)
    user = m.ForeignKey(CustomUser, on_delete=m.CASCADE, null=True, default=None)
    verification_code = m.CharField(max_length=32, null=True, blank=True, default=None)
