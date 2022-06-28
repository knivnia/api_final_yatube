from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post
from . import serializers
from .permissions import MethodsAndIsAdminUser, UserIsAuthor


class PerformCreateMixin:
    def perform_create(self, serializer):
        current_user_field = type(self).__dict__.get('current_user_field')
        if current_user_field is None:
            raise NotImplementedError('current_user_field is not implemented!')
        elif not hasattr(serializer.Meta.model, current_user_field):
            raise AttributeError(f'Model {serializer.Meta.model} has'
                                 f'no attribute {current_user_field}!')
        else:
            serializer.validated_data[current_user_field] = self.request.user
        serializer.save()


class PostViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [UserIsAuthor, ]
    pagination_class = LimitOffsetPagination
    current_user_field = 'author'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [MethodsAndIsAdminUser, ]


class CommentViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [UserIsAuthor, ]
    current_user_field = 'author'

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.validated_data['post'] = get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )
        super(CommentViewSet, self).perform_create(serializer)


class FollowViewSet(PerformCreateMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=user__username', '=following__username')
    current_user_field = 'user'

    def get_queryset(self):
        return self.request.user.follower.all()
