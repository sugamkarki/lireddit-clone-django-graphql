import graphene
from django.contrib.auth.models import User

from posts import models
from .types import PostType

class CreatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        body = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, title, body, created_by=1):
        # print(info.context.user)
        post = models.Post(title=title, body=body)
        user = User.objects.get(id=created_by)
        post.created_by = user
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        body = graphene.String()
        # image=graphene.Field(Pro)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, title=None, body=None):
        # print(info.context.user)
        post = models.Post.objects.get(pk=id)
        post.title = title if title is not None else post.title
        post.body = body if body is not None else post.body
        # post.title = title if title is not None else post.title
        # if title is not None:
        #     post.title = title
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id):
        post = models.Post.objects.get(pk=id)
        if post is not None:
            post.delete()
        return
