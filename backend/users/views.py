from django.contrib.auth.tokens import default_token_generator
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Subscription
from .serializers import (CustomUserSerializer, SubscriptionSerializer,
                          TokenSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


class APIGetToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser, email=serializer.validated_data['email']
        )
        if default_token_generator.check_token(
            user, serializer.validated_data['password']
        ):
            return Response(get_tokens_for_user(user))
        return Response(
            {'password': "password doesn't match"}
        )


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomUserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        subquery = Subscription.objects.filter(
            user=self.request.user, author=OuterRef('id')
        )
        return CustomUser.objects.annotate(is_subscribed=Exists(subquery))
