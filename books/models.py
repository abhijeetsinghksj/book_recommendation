# books/models.py
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.URLField()
    ratings = models.FloatField(default=0)
    genre = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_genre = models.CharField(max_length=100)
    favorite_author = models.CharField(max_length=100)
    favorite_publication_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"

# models.py


class BookRecommendation(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.URLField()
    ratings = models.IntegerField()
    genre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title



class RecommendedBook(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    cover_image_url = models.URLField()
    ratings = models.IntegerField()
    genre = models.CharField(max_length=50)

