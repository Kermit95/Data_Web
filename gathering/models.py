from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face = models.ImageField(upload_to='profile_images', blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


class DataTable(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    major_id = models.TextField(max_length=4, null=False)
    minor_id = models.TextField(max_length=4, null=False)
    name = models.TextField(max_length=200, null=False)
    sample = models.TextField(null=False)
    contents = models.TextField()
    slug = models.SlugField()

    def save (self, *arg, **kwargs):
        self.slug = slugify(self.name)
        super(DataTable, self).save(*arg, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'datatables'
