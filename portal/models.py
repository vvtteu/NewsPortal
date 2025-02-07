from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 0
        for post in self.post_set.all():
            post_rating += post.rating * 3

        comment_rating = 0
        for comment in self.user.comment_set.all():
            comment_rating += comment.rating

        post_comment_rating = 0
        for post in self.post_set.all():
            for comment in post.comment_set.all():
                post_comment_rating += comment.rating

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscriber')

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    POST_CHOICES = [
        ('article', 'Статья'),
        ('news', 'Новость'),
    ]
    post_type = models.CharField(max_length=10, choices=POST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124]
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
