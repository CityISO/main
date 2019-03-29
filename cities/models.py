from django.db import models

BASE_CITY_UPLOAD_DIR = 'city/'


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


class CityPeoplePhoto(models.Model):
    city = models.ForeignKey(City, models.SET_NULL, null=True, verbose_name="город")
    added = models.DateTimeField(auto_now_add=True, verbose_name="добавлено")
    photo = models.ImageField(verbose_name="портерт из фотографий", upload_to=BASE_CITY_UPLOAD_DIR + "portrait/")

    def __str__(self):
        return self.city.name + " " + str(self.added)

    class Meta:
        verbose_name = 'Жители города в коллаже'
        verbose_name_plural = 'Жители городов в коллажах'