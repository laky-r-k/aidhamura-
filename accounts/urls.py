from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view,name="login"),
    path('signup/',views.signup_view,name="signup"),
    path('logout/',views.logout_view,name='logout'),
    path('profile/<str:username>',views.profile_view,name='profile'),
    path('add_friend/<str:username>/', views.add_friend, name='add_friend'),
    path('remove_friend/<str:username>/', views.remove_friend, name='remove_friend'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
