from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # logo = models.ImageField(blank=True)
    logo_path = models.CharField(max_length=200)
    employee = models.IntegerField()
    work_year = models.FloatField()


class Report(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=250)
    date = models.DateField()
    author = models.CharField(max_length=100)
    firm = models.CharField(max_length=250)


class Gongo(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    bookmark_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmark_gongos')
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    no = models.CharField(max_length=250)
    url = models.URLField(max_length=250)
    image = models.URLField(max_length=250)
    date = models.DateField()
    dday = models.IntegerField()
    # updated_at = models.DateTimeField(auto_now=True)


class Article(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=250)
    press = models.CharField(max_length=250)
    date = models.DateTimeField()


class Finance(models.Model):
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    capital = models.IntegerField()
    revenue = models.IntegerField()
    profit = models.IntegerField()
    debt = models.FloatField()
    year = models.IntegerField()