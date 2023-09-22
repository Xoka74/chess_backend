from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views
router = DefaultRouter()
router.register('friends', views.FriendRetrieveListViewSet, basename='friends')
router.register('requests', views.FriendRequestsViewSet, basename='requests')

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     # path('', views.profile, name='users'),
#     # path('sign-up', views.sign_up, name='sign-up'),
#     # path('sign-in', views.sign_in, name='sign-in'),
#     # path('sign-out', views.sign_out, name='sign-out'),
#     path('', views.profile, name='users'),
# ]
