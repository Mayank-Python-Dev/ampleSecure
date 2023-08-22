from django.urls import path
from .views import (
    UserRegistration,
    UserLogin,
    UserGroup,
    UsersWithGroup,
    UserStatus
)

urlpatterns = [

    path('registration/',UserRegistration.as_view(),name="account-registration"),
    path('login/', UserLogin.as_view(), name='account-login'),
    path('group_list/',UserGroup.as_view(), name='group-list'),
    path('get_users_list/',UsersWithGroup.as_view(), name='users-list'),
    path('update_user_status/<str:uid>/',UserStatus.as_view(),name="update-user-status"),
    
]