from .views import AuthAPIView,TasksAPIView,UserListAPIView,LogoutAPIView
from django.urls import path


urlpatterns=[
    path("login",AuthAPIView.as_view(),name="login"),
    path("tasks",TasksAPIView.as_view(),name="tasks"),
    path("tasks/<int:id>",TasksAPIView.as_view(),name="tasks_id"),
    path("users",UserListAPIView.as_view(),name='user_list'),
    path("logout",LogoutAPIView.as_view(),name='logout')
]