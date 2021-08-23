import graphene
from django.contrib.auth.models import User
from graphql import GraphQLError
from posts import models
from .types import PostType, LikeType, CommentType
from graphql_jwt.decorators import login_required


class CreatePost(graphene.Mutation):
    class Arguments:
        # post_id = graphene.ID()
        title = graphene.String()
        body = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    @login_required
    def mutate(cls, root, info, title, body):
        if info.context.user:
            print(info.context.user.id)
        # print(request.user.username)
        post = models.Post(title=title, body=body)
        user = User.objects.get(id=info.context.user.id)
        is_verified = user.status.verified
        if not is_verified:
            raise GraphQLError("You Are Not verified")

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
    @login_required
    def mutate(cls, root, info, post_id, title=None, body=None):
        post = models.Post.objects.get(pk=post_id)
        user = info.context.user
        if post.user.id != user.id:
            raise GraphQLError("This is not your post")
        post.title = title if title is not None else post.title
        post.body = body if body is not None else post.body
        # if title is not None:
        #     post.title = title
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID()

    post = graphene.Field(PostType)

    @classmethod
    @login_required
    def mutate(cls, root, info, post_id):
        post = models.Post.objects.get(pk=post_id)
        if post is not None:
            user = info.context.user
            print(user.id)
            print(post.created_by.id)
            if post.created_by.id == user.id:
                print("equallll")
                post.delete()
                return
            else:
                raise GraphQLError("This is not your post")

        raise GraphQLError("No Post Exists")


class LikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID()

    post = graphene.Field(PostType)

    @classmethod
    @login_required
    def mutate(cls, root, info, post_id):
        user = models.User.objects.get(pk=info.context.user.id)
        is_verified = user.status.verified
        if not is_verified:
            raise GraphQLError("You Are Not verified")

        post = models.Post.objects.get(pk=post_id)
        like = models.Like.objects.filter(user=user, post=post)
        if like:
            like.delete()
            return
        like = models.Like(post=post, user=user)
        like.save()
        return LikePost(post=post)


class CommentPost(graphene.Mutation):
    class Arguments:
        post_id = graphene.ID()
        body = graphene.String()

    post = graphene.Field(CommentType)

    @classmethod
    @login_required
    def mutate(cls, root, info, post_id, body):
        user = models.User.objects.get(pk=info.context.user.id)
        is_verified = user.status.verified
        if not is_verified:
            raise GraphQLError("You Are Not verified")

        post = models.Post.objects.get(pk=post_id)
        comment = models.Comment(body=body, user=user, post=post)
        comment.save()
        return CommentPost(post=comment)
