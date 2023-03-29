from django.db import models as m

from core.models import CustomUser
from goals.models import BaseModel, Board


class Goal(BaseModel):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(m.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(m.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = m.CharField(verbose_name='Название', max_length=255)
    description = m.TextField(verbose_name='Описание', null=True, blank=True)
    category = m.ForeignKey(to='GoalCategory', verbose_name='Категория', on_delete=m.CASCADE, related_name='goals')
    status = m.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    priority = m.PositiveSmallIntegerField(verbose_name='Приоритет', choices=Priority.choices, default=Priority.medium)
    due_date = m.DateTimeField(verbose_name='Дата выполнения', null=True, blank=True)
    user = m.ForeignKey(CustomUser, on_delete=m.PROTECT, verbose_name='Автор', related_name='goals')

    def __str__(self):
        return self.title


class GoalCategory(BaseModel):
    title = m.CharField(verbose_name='Название', max_length=255)
    user = m.ForeignKey(CustomUser, verbose_name='Автор', on_delete=m.PROTECT)
    is_deleted = m.BooleanField(verbose_name='Удалена', default=False)
    board = m.ForeignKey(Board, verbose_name='Доска', on_delete=m.PROTECT, related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class GoalComment(BaseModel):
    user = m.ForeignKey(CustomUser, on_delete=m.PROTECT, verbose_name='Автор', related_name='comments')
    goal = m.ForeignKey(Goal, verbose_name='Цель', on_delete=m.CASCADE, related_name='comments')
    text = m.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
