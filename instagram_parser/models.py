from django.db import models

from cities.models import City


class InstagramPost(models.Model):
    # todo think about unique
    city = models.ForeignKey(to=City, on_delete=models.SET_NULL, null=True, verbose_name="город")

    shortcode = models.SlugField(verbose_name='Шорткод',
                                 max_length=124, unique=True)
    text = models.TextField(verbose_name='Текст')

    likes = models.PositiveIntegerField(verbose_name='Кол-во лайков')
    comments_count = models.PositiveIntegerField(verbose_name='Кол-во комментов')

    # https://stackoverflow.com/questions/15470180/character-limit-on-instagram-usernames
    owner = models.TextField(verbose_name='Владелец', max_length=35)
    timestamp = models.DateTimeField()  # todo
    post_lat = models.FloatField()
    post_lon = models.FloatField()
    processed = models.BooleanField(verbose_name='Обработано',
                                    default=False)
    is_ad = models.BooleanField(verbose_name='Рекламная запись',
                                default=False)

    def instagram_link(self):
        return f'https://instagram.com/p/{self.shortcode}/'

    def __str__(self):
        return 'Пост: ' + str(self.shortcode)

    class Meta:
        verbose_name = 'Пост в инстаграме'
        verbose_name_plural = 'Посты в инстаграме'


class InstagramPostAnalysis(models.Model):
    post = models.ForeignKey(InstagramPost, models.CASCADE)
    sentiment_score = models.FloatField()

    def __str__(self):
        return "Результат %s" % self.post.shortcode

    class Meta:
        verbose_name = 'Результат анализа поста'
        verbose_name_plural = 'Результаты анализа постов'


class InstagramPostsThematic(models.Model):
    city = models.ForeignKey(to=City, on_delete=models.SET_NULL, null=True, verbose_name="город")

    from_time = models.DateField(verbose_name="начало")
    to_time = models.DateField(verbose_name="конец")

    themes = models.TextField(verbose_name="темы")

    def __str__(self):
        return self.city.name + " " + self.themes[:30]
