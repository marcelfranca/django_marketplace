from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


def download_media_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_product", blank=True)
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(default='Default Value')
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)
    sale_price = models.DecimalField(max_digits=100, decimal_places=2, default=6.99,
                                     null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        view_name = "products:detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def thumbnail_location(instance, filename):
    return "%s/%s" %(instance.product.slug, filename)


THUMB_CHOICES = (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)


class Thumbnail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(
        width_field="width", height_field="height",
        blank=True, null=True, upload_to=thumbnail_location)

    def __str__(self):
        return str(self.media.path)


import os
import shutil
from PIL import Image
import random

from django.core.files import File



def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.media:
        hd = Thumbnail.objects.get_or_create(product=instance, type='hd')[0]
        sd = Thumbnail.objects.get_or_create(product=instance, type='sd')[0]
        micro = Thumbnail.objects.get_or_create(product=instance, type='micro')[0]

        hd_max = (400, 400)
        sd_max = (200, 200)
        micro_max = (50, 50)

        print(instance.media.path)

        filename = os.path.basename(instance.media.path)
        thumb = Image.open(instance.media.path)
        thumb.thumbnail(hd_max, Image.ANTIALIAS)

        temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT)

        if not os.path.exists(temp_loc):
            os.makedirs(temp_loc)

        temp_file_path = os.path.join(temp_loc, filename)
        if os.path.exists(temp_file_path):
            temp_path = os.path.join(temp_loc, "%s" %(random.random()))
            os.makedirs(temp_path)
            temp_file_path = os.path.join(temp_path, filename)

        temp_image = open(temp_file_path, "w")
        thumb.save(temp_image)
        thumb_data = open(temp_file_path, "r")

        thumb_file = File(thumb_data)
        hd.media.save(filename, thumb_file)
        # shutil.rmtree(temp_loc, ignore_errors=True)


post_save.connect(product_post_save_receiver, sender=Product)



# def product_post_save_receiver(sender, instance, *args, **kwags):
#     if instance.slug != slugify(instance.title):
#         instance.slug = slugify(instance.title)
#         instance.save()
#
#
# post_save.connect(product_post_save_receiver, sender=Product)
