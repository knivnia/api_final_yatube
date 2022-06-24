from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post
from . import serializers
from .permissions import MethodsAndIsAdminUser, UserIsAuthor


class PerformCreateMixin:
    def perform_create(self, serializer):
        if isinstance(self, PostViewSet):
            serializer.save(author=self.request.user)
        elif isinstance(self, CommentViewSet):
            post_id = self.kwargs.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            serializer.save(author=self.request.user, post=post)
        else:
            if serializer.is_valid():
                serializer.save(user=self.request.user)


class PostViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [UserIsAuthor, ]
    pagination_class = LimitOffsetPagination


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [MethodsAndIsAdminUser, ]


class CommentViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [UserIsAuthor, ]

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()


class FollowViewSet(PerformCreateMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=user__username', '=following__username')

    def get_queryset(self):
        return self.request.user.follower.all()
