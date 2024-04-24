from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True, blank=False, null=False, unique=True)
    fam = models.CharField(max_length=100, verbose_name='surname')
    name = models.CharField(max_length=200, verbose_name='name')
    otc = models.CharField(max_length=200, blank=True, null=True, verbose_name='patronymic')
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=20)


class Coord(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    DIFFICULTY_LEVEL = (
        ('1A', '1A'),
        ('1Б', '1Б'),
        ('2A', '2A'),
        ('2Б', '2Б'),
        ('3A', '3A'),
        ('3Б', '3Б')
    )

    spring = models.CharField(max_length=2, choices=DIFFICULTY_LEVEL)
    summer = models.CharField(max_length=2, choices=DIFFICULTY_LEVEL)
    autumn = models.CharField(max_length=2, choices=DIFFICULTY_LEVEL)
    winter = models.CharField(max_length=2, choices=DIFFICULTY_LEVEL)


class Image(models.Model):
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    data = models.ImageField(upload_to="uploads/")


class PerevalAdded(models.Model):

    STATUS = (
        ('new', 'Создан'),
        ('pending', 'На проверке'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено')
    )

    beauty_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=100)
    connect = models.CharField(max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    coords = models.ForeignKey(Coord, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    images = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)



