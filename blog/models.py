from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_post_pics', null=True, blank=True)

    def __str__(self):
        return self.title

class Blogcomment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10]
    
class BlogCommentReply(models.Model):
    text = models.TextField()
    blogcomment = models.ForeignKey(Blogcomment, on_delete=models.CASCADE, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
