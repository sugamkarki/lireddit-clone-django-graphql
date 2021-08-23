import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from posts import models


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post
        fields = "__all__"


class CommentType(DjangoObjectType):
    class Meta:
        model = models.Comment
        fields = "__all__"


class LikeType(DjangoObjectType):
    class Meta:
        model = models.Like
        fields = "__all__"


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username",)
