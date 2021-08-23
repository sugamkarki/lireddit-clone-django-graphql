import graphene
from . import models
from .mutations import PostType, LikeType, CommentType, LikePost, CommentPost
from graphql_auth import mutations
from .mutations import CreatePost, UpdatePost, DeletePost
from graphql_auth.schema import MeQuery


class Query(MeQuery, graphene.ObjectType):
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)
    likes = graphene.List(LikeType)
    post = graphene.Field(PostType, id=graphene.Int())
    comment = graphene.Field(CommentType, id=graphene.Int())
    like = graphene.Field(LikeType, id=graphene.Int())

    def resolve_posts(root, info):
        posts = models.Post.objects.all()
        return posts

    def resolve_comment(root, info, id):
        return models.Comment.objects.get(pk=id)

    def resolve_like(root, info, id):
        return models.Like.objects.get(pk=id)

    def resolve_comments(root, info):
        return models.Comment.objects.all()

    def resolve_likes(root, info):
        return models.Like.objects.all()


class Mutation(graphene.ObjectType):
    add_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    like_post = LikePost.Field()
    comment_post = CommentPost.Field()
    # mutations inbuilt functions
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    login = mutations.ObtainJSONWebToken.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
