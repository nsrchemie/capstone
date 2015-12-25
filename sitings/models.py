from django.db import models
from django.utils.timezone import now as timezone_now

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone_now)
    published_date = models.DateTimeField(blank=True, null=True)
    picture = models.ImageField(upload_to="%Y/%m/%d", blank=True, null=True)
    location = models.CharField(max_length=200)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title