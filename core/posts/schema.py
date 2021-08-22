import graphene
from graphene_django import DjangoObjectType
from . import models


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


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    all_comments = graphene.List(CommentType)
    all_likes = graphene.List(LikeType)

    def resolve_all_posts(root, info):
        return models.Post.objects.all()

    def resolve_all_comments(root, info):
        return models.Comment.objects.all()

    def resolve_all_likes(root, info):
        return models.Like.objects.all()


schema = graphene.Schema(query=Query)
