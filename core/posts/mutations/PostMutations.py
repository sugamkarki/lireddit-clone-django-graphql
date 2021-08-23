import graphene
from django.contrib.auth.models import User

from posts import models
from .types import PostType, LikeType, CommentType


class CreatePost(graphene.Mutation):
    class Arguments:
        # post_id = graphene.ID()
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
        post_id = graphene.ID()
        title = graphene.String()
        body = graphene.String()
        # image=graphene.Field(Pro)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, post_id, title=None, body=None):
        # print(info.context.user)
        post = models.Post.objects.get(pk=post_id)
        post.title = title if title is not None else post.title
        post.body = body if body is not None else post.body
        # post.title = title if title is not None else post.title
        # if title is not None:
        #     post.title = title
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, post_id):
        post = models.Post.objects.get(pk=post_id)
        if post is not None:
            post.delete()
        return


class LikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID()

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, post_id):
        user = models.User.objects.get(pk=info.context.user.id)
        post = models.Post.objects.get(pk=post_id)
        like = models.Like.objects.filter(user=user, post=post)
        if like:
            like.delete()
            return
        like = models.Like(post=post, user=user)
        like.save()
        return LikePost(post=like)


class CommentPost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID()
        body = graphene.String()
    post = graphene.Field(CommentType)
    @classmethod
    def mutate(cls, root, info, post_id, body):
        user = models.User.objects.get(pk=info.context.user.id)
        post = models.Post.objects.get(pk=post_id)
        comment = models.Comment(body=body, user=user, post=post)
        comment.save()
        return CommentPost(post=comment)
