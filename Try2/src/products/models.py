from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(default='Product description Here')
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)
    sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)

    def __str__(self):
        return self.title
