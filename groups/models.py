from django.db import models


# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наименование группы', null=True)
    users_count = models.IntegerField(null=True, verbose_name='Количество участников')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title
