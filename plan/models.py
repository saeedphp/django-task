from django.db import models

# Create your models here.

class Plan(models.Model):
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d', null=True, blank=True)
    banner = models.ImageField(upload_to='banners/%Y/%m/%d', null=True, blank=True)
    target_price = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.title} - {self.start_date} - {self.end_date}'