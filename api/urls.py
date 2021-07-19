from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, EmailConfirmation,
                    GenreViewSet, ReviewViewSet, TitleViewSet, TokenObtain,
                    UserViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, 'review')
v1_router.register(
    r'titles/\d+/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, 'comment')

auth_patterns = [
    path('email/', EmailConfirmation.as_view(), name='email_confirmation'),
    path('token/', TokenObtain.as_view(), name='token_obtain'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
