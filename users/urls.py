from django.urls import path
from .views import signup_view, login_view, logout_view, user_detail_view, UsersListView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/', user_detail_view, name ='user_detail'),
    path('users/', UsersListView.as_view(), name='users-list'),
]
