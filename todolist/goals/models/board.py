from django.db import models as m

from core.models import CustomUser
from goals.models import BaseModel


class Board(BaseModel):
    title = m.CharField(verbose_name='Название', max_length=255)
    is_deleted = m.BooleanField(verbose_name='Удалена', default=False)

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'


class BoardParticipant(BaseModel):
    class Role(m.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = m.ForeignKey(Board, verbose_name='Доска', on_delete=m.PROTECT, related_name='participants')
    user = m.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=m.PROTECT, related_name='participants')
    role = m.PositiveSmallIntegerField(verbose_name='Роль', choices=Role.choices, default=Role.owner)

    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
