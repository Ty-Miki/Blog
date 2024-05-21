from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    # Add a status field to posts
    class Status(models.TextChoices):
        # NAME = "value", "label"
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    # attributes a post should include.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()

    # date metadata associated with a post.
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # data to indicate post status.
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    # Register model managers.
    objects = models.Manager() # The default model manager.
    published = PublishedManager() # Custom model manager to access published posts.

    # Specify a default query ordering and add database index.
    class Meta:
        ordering = ["-publish"]
        indexes = [models.Index(fields=["-publish"]), ]

    # Change post objects name to a human readable format.
    def __str__(self):
        return self.title
