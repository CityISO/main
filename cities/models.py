from django.db import models


class City(models.Model):
    name = models.TextField(max_length=256, unique=True, verbose_name="название")
    image = models.ImageField(verbose_name="главная картинка")
    image_preview = models.ImageField(verbose_name="картинка для превью")
    small_description = models.TextField(max_length=256, verbose_name="краткое описание")
    description = models.TextField(verbose_name="полное описание")
    active = models.BooleanField(verbose_name="показывать пользователю", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"
