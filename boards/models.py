from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from accounts.models import User
from tags.models import Tag

from hitcount.models import HitCount, HitCountMixin

class Board(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)


class Post(models.Model, HitCountMixin):
    board = models.ForeignKey(Board, related_name='posts')
    title = models.CharField(max_length=128)
    author = models.ForeignKey(User)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='posts')

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, self.title)


class Comment(models.Model):
    parent = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=250)
    
    def __str__(self):
        return '<%s %s>' % (self.__class__.__name__, self.parent.title)

# TODO: 댓댓글 여부
