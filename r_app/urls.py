from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("main/", views.main_page, name="main-page"),
    path("user/", views.users_page, name="user-page"),
    path("api/", views.api_page, name="api_page"),
    path("api/login/", views.login_view, name="api_login"),
    path("create_user/", views.create_user, name="create_user_api"),
    path("update_user/", views.update_user, name="update_user"),
    path("delete_user/", views.delete_user, name="delete_user"),
    path("create_api/", views.create_api, name="create_api"),
    path("update_api/", views.update_api, name="update_api"),
    path("delete_api/", views.delete_api, name="delete_api"),
    path("get_api/", views.view_api, name="view_api"),
    path("get_user/", views.view_user, name="view_user"),
    path("get_userBy/", views.get_userById, name="get_user_by_id"),
    path("get_apiBy/", views.get_apiById, name="get_user_by_id"),
    path("mapApi/", views.mappingAPI_User, name="mapping_user"),
]
