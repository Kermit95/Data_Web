from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face = models.ImageField(upload_to='profile_images', blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


class DataTableOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=50, null=False, default='')

    def __str__(self):
        return self.name


class DataTable(models.Model):
    owner = models.ForeignKey(DataTableOwner, on_delete=models.CASCADE)
    serial_key = models.TextField(max_length=32, unique=True, null=False, default='')
    name = models.TextField(max_length=200, null=False, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    head = models.TextField(null=False, default='')
    sample = models.TextField(null=False)
    slug = models.SlugField()

    def save (self, *arg, **kwargs):
        self.slug = slugify(self.name)
        super(DataTable, self).save(*arg, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'datatables'


class DataTableItem(models.Model):
    datatable = models.ForeignKey(DataTable, on_delete=models.CASCADE)
    order_num = models.IntegerField(null=False, default=0)
    content = models.TextField()

    def __str__(self):
        return 'Belongs to ' + self.datatable.name
