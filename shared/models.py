from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=512, verbose_name="название", unique=True, null=False)
    value = models.TextField(verbose_name="значение", null=False)
    description = models.TextField(verbose_name="описание", null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'
