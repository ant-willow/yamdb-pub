from django.core.mail import send_mail
from django.db.models import Avg
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import IsAdmin, IsModerator, IsOwner, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          CommonTitleSerializer, GenreSerializer,
                          PostTitleSerializer, ReviewSerializer,
                          TokenObtainSerializer, UserSerializer)


class EmailConfirmation(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': email},
            )
            send_mail('subject', user.confirmation_key,
                      'admin@yamdb.fake', (email,))
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class TokenObtain(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('confirmation_code')
        serializer = TokenObtainSerializer(data={'email': email, 'code': code})
        serializer.is_valid(raise_exception=True)
        user = serializer.user.first()
        user.confirm_email(code)
        refresh = RefreshToken.for_user(user)
        data = {'token': str(refresh.access_token)}
        return Response(data=data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = "username"
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def me_update(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects.all()
                .annotate(rating=Avg('reviews__score')))
    permission_classes = [IsAuthenticated & IsAdmin | ReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return PostTitleSerializer
        return CommonTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner | IsModerator]

    def perform_create(self, serializer):
        try:
            title = get_object_or_404(Title, pk=self.kwargs['title_id'])
            serializer.save(author=self.request.user, title=title)
        except IntegrityError:
            raise ValidationError()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        reviews = title.reviews.all()
        return reviews


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner | IsModerator]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user,
                        review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        comments = review.comments.all()
        return comments


class ListCreateDestroyViewSet(viewsets.GenericViewSet,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated & IsAdmin | ReadOnly]
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
