from django.db import models

# Create your models here.


class KeyWords(models.Model):
    name = models.CharField(max_length=255, blank=False)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'KeyWord: {self.name}, status: {self.status}'

    class Meta():
        verbose_name = 'KeyWord'
        verbose_name_plural = 'KeyWords'


class Links(models.Model):
    name = models.CharField(max_length=255, blank=False)
    link = models.TextField(blank=False)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Link: {self.name}, status: {self.status}'

    class Meta():
        verbose_name = 'Link'
        verbose_name_plural = 'Links'


class ProductInfo(models.Model):
    product_name = models.CharField(max_length=255, blank=False)
    current_price = models.IntegerField(blank=False)
    link = models.TextField(blank=False)
    reviews = models.IntegerField(blank=False)
    features = models.TextField(blank=False)

    def __str__(self) -> str:
        return self.product_name

    class Meta():
        verbose_name = 'Item'
        verbose_name_plural = 'Items'




