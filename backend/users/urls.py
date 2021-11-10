from django.urls import include, path

from .views import CustomUserListView, SubscriptionAPIView

urlpatterns = [
    path('users/<int:id>/subscribe/',
         SubscriptionAPIView.as_view(),
         name='subscribe'),
    path('users/subscriptions/',
         CustomUserListView.as_view(),
         name='subscriptions'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
