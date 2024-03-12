from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse
      
class Article(models.Model):
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=255, default="No description")
  imageLink = models.CharField(max_length=255, null=True)
  content = HTMLField()
  date = models.DateField(auto_now_add=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  featured = models.BooleanField(default=False)
  category = models.CharField(max_length=255, default='uncategorized')
  likes = models.ManyToManyField(User, related_name='likes', blank=True)

class Category(models.Model):
  name = models.CharField(max_length=255)
  
  def __str__(self):
    return self.name
  def get_absolute_url(self):
			return reverse("home")

class Comment(models.Model):
  article = models.ForeignKey(Article, related_name="comments" , on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Comment by {self.user.username} on {self.article.title}'

