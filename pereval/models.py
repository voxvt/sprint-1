from django.db import models
from django.conf import settings



class Users(models.Model):
    email = models.EmailField(max_length=128, verbose_name='Электронная почта')
    fam = models.CharField(max_length=40, verbose_name='Фамилия')
    name = models.CharField(max_length=40, verbose_name='Имя')
    pat = models.CharField(max_length=40, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Турист'
        verbose_name_plural = 'Туристы'

    def __str__(self):
        return f'{self.fam}{self.name}{self.pat}'


class Pereval(models.Model):
    NEW = 'NW'
    PENDING = 'PN'
    ACCEPTED = 'AC'
    REJECTED = 'RJ'

    STATUS_CHOICES = [
        (NEW, 'новый'),
        (PENDING, 'модератор взял в работу'),
        (ACCEPTED, 'модерация прошла успешно'),
        (REJECTED, 'модерация прошла, информация не принята'),
    ]

    CONNECTION = 'connection'
    DISCONNECT = 'disconnect'
    UNSTABLE_CONNECTION = 'unstable connection'

    CONNECT_CHOICES = [
        (CONNECTION, 'Connection'),
        (DISCONNECT, 'Disconnect'),
        (UNSTABLE_CONNECTION, 'Unstable Connection'),
    ]

    beauty_title = models.CharField(max_length=128, verbose_name='Тип объекта')
    title = models.CharField(max_length=128, verbose_name='Название объекта')
    other_titles = models.CharField(max_length=128, verbose_name='Другое название')
    connect = models.CharField(max_length=32, choices=CONNECT_CHOICES, verbose_name='Подключение')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    coord = models.OneToOneField('Coords', on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, verbose_name='Турист')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=NEW, verbose_name='Статус записи')
    level = models.ForeignKey('Level', on_delete=models.CASCADE, verbose_name='Уровень сложности')

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

    def __str__(self):
        return f'{self.pk} {self.beauty_title}{self.status}'



class Coords(models.Model):
    latitude = models.DecimalField(decimal_places=8, max_digits=10, verbose_name='Широта')
    longitude = models.DecimalField(decimal_places=8, max_digits=10, verbose_name='Долгота')
    height = models.IntegerField(default=0, verbose_name='Высота')

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return f'Широта: {self.latitude} Долгота: {self.longitude} Высота: {self.height}'


class Level(models.Model):
    WINTER = '4A'
    SPRING = '2A'
    SUMMER = '1A'
    AUTUMN = '3A'

    LEVEL_CHOICES = (
        ('1A', '1A'),
        ('2A', '2A'),
        ('3A', '3A'),
        ('4A', '4A'),
    )

    winter_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=WINTER, verbose_name='Зима')
    spring_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=SPRING, verbose_name='Весна')
    summer_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=SUMMER, verbose_name='Лето')
    autumn_lev = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=AUTUMN, verbose_name='Осень')

    class Meta:
        verbose_name = 'Уровень сложности'
        verbose_name_plural = 'Уровни сложности'

    def __str__(self):
        return (
            f'Зима: {self.winter_lev} '
            f'Весна: {self.spring_lev} '
            f'Лето: {self.summer_lev} '
            f'Осень: {self.autumn_lev}'
        )




class Images(models.Model):
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=128)
    pereval_id = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.title


