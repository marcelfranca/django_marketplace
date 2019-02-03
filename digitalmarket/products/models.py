from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, default='slug-field')
    description = models.TextField(default='Default Value')
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)
    sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99,
                                     null=True, blank=True)

    def __str__(self):
        return self.title
