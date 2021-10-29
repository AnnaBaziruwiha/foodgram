from django.db.models import Exists, OuterRef
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser, Subscription
from .serializers import CustomUserSerializer, SubscriptionSerializer


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
