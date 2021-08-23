from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    class Meta:
        verbose_name_plural = "Posts"

    title = models.CharField(max_length=255, blank=False)
    body = models.TextField()
    image = models.ImageField(blank=True, default=None, null=True, upload_to='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title


class Like(models.Model):
    class Meta:
        verbose_name_plural = "Likes"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    class Meta:
        verbose_name_plural = "Comments"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
