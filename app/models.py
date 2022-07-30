from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='images', null=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def get_formatted_date(self):
        return self.created_on.strftime("%Y-%m-%d %H:%M:%S")

    def save(self, *args, **kwargs):  
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)  

    @property
    def number_of_comments(self):
        return Comment.objects.filter(blogpost_connected=self).count()  


class Comment(models.Model):
    blogpost_connected = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]


