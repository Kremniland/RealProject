from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class Organisation(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    director = models.ForeignKey(
        to=User, on_delete=models.RESTRICT, related_name='organisation_directors',
        verbose_name='Директор'
    )
    employees = models.ManyToManyField(
        to=User, related_name='organisation_employees', verbose_name='Сотрудники',
        blank=True,
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Group(models.Model):
    organisation = models.ForeignKey(
        to=Organisation, on_delete=models.CASCADE, related_name='groups',
        verbose_name='Организация',
    )
    name = models.CharField(verbose_name='Название', max_length=255)
    manager = models.ForeignKey(
        to=User, on_delete=models.RESTRICT, related_name='group_managers',
        verbose_name='Менеджер',
    )
    employees = models.ManyToManyField(
        to=User, related_name='group_employees', verbose_name='Сотрудники',
        blank=True,
    )
    min_active = models.PositiveSmallIntegerField(
        verbose_name='Минимальное количество активных сотрудников', null=True, blank=True,
    )
    break_start = models.TimeField(verbose_name='Начало обеда', null=True, blank=True, )
    break_end = models.TimeField(verbose_name='Конец обеда', null=True, blank=True, )
    break_max_duration = models.PositiveSmallIntegerField(
        verbose_name='Максимальная длительность обеда', null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class ReplacementStatus(models.Model):
    code = models.CharField(verbose_name='Код', max_length=16, primary_key=True)
    name = models.CharField(verbose_name='Название', max_length=32, )
    sort = models.PositiveSmallIntegerField(verbose_name='Сортировка', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активность', default=True)

    class Meta:
        verbose_name = 'Статус смены'
        verbose_name_plural = 'Статусы смены'
        ordering = ('sort',)

    def __str__(self):
        return f'{self.code} для {self.name}'


class Replacement(models.Model):
    group = models.ForeignKey(
        to=Group, on_delete=models.CASCADE, related_name='replacements',
        verbose_name='Группа'
    )
    date = models.DateField(verbose_name='Дата смены')
    break_start = models.TimeField(verbose_name='Начало обеда')
    break_end = models.TimeField(verbose_name='Конец обеда')
    break_max_duration = models.PositiveSmallIntegerField(
        verbose_name='Макс. продолжительность обеда'
    )

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'
        ordering = ('-date',)

    def __str__(self):
        return f'Смена №{self.pk} для {self.group}'


class ReplacementEmployee(models.Model):
    employee = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='replacements',
        verbose_name='Сотрудник'
    )
    replacement = models.ForeignKey(
        to=Replacement, on_delete=models.CASCADE, related_name='employees',
        verbose_name='Смена'
    )
    status = models.ForeignKey(
        to=ReplacementStatus, on_delete=models.RESTRICT, related_name='replacement_employees',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Смена - Работник'
        verbose_name_plural = 'Смены - Работники'

    def __str__(self):
        return f'Смена {self.replacement} для {self.employee}'

