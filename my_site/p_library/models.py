from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    age = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.age} years old'


class Authors(models.Model):
    """ Author model """
    full_name = models.TextField(max_length=50)
    birth_year = models.SmallIntegerField()
    country = models.CharField(max_length=2)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    """ Book model """
    ISBN = models.CharField(max_length=13)
    title = models.CharField(max_length=128)
    description = models.TextField()
    year_release = models.SmallIntegerField()
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, default='')
    copy_count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    redaction = models.ForeignKey('Redaction', on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    reader = models.ForeignKey('Reader', on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    image = models.ImageField(upload_to='media', default='default.png')

    def __str__(self):
        return self.title


class Inspiration(models.Model):
    """ Inspiration model """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    inspirer = models.ForeignKey(
        Authors,
        on_delete=models.CASCADE,
        related_name='inspired_works',
    )

    def __str__(self):
        return f'{self.book} - {self.author} - {self.inspirer}'


class Redaction(models.Model):
    """ Redaction model """
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Reader(models.Model):
    """ Reader model """
    full_name = models.TextField()
    birth_year = models.SmallIntegerField()

    def __str__(self):
        return self.full_name
