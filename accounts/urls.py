from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [

    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('user_view/', views.user_view, name='user_view'),
    path('logout/', views.logout_request, name='logout'),

]