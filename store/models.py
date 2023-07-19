from django.db import models
from django.db.models.signals import post_save, pre_save
from utils.slug_generate import  unique_slug_generator
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Store(models.Model):
    OFF_DAYS = [
        ("SATURDAY", "Saturday"),
        ("SUNDAY", "Sunday"),
        ("MONDAY", "Monday"),
        ("TUESDAY", "Tuesday"),
        ("WEDNESDAY", "Wednesday"),
        ("THURSDAY", "Thursday"),
        ("FRIDAY", "Friday"),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True,
                            max_length = 255)
    type = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField()
    primary_phone = models.CharField(max_length=50)
    secondary_phone = models.CharField(max_length=50, null=True, blank=True)
    map_link = models.URLField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    shown_in_website = models.BooleanField(default=True)
    # off_days = ArrayField(models.CharField(choices=OFF_DAYS, max_length=50),
    #                       blank=True, default=list)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    invoice_no = models.CharField(max_length=255)

    def __str__(self):
        return self.invoice_no
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,on_delete=models.SET_NULL, 
        null=True,blank=True)
    selling_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.order.invoice_no

# ..........***.......... Book Category ..........***..........


def store_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        title = slugify(instance.name.lower()[:17])
        slug_binding = title + '-' + unique_slug_generator()
        instance.slug = slug_binding


pre_save.connect(store_slug_pre_save_receiver, sender=Store)
