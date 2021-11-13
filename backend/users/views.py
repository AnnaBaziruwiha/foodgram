from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Subscription
from .serializers import CustomUserListSerializer, SubscriptionSerializer


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        data = {
            'user': request.user.id,
            'author': id
        }
        serializer = SubscriptionSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        author = get_object_or_404(CustomUser, id=id)
        subscription = get_object_or_404(
            Subscription, user=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserListSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(followed__user=user)
