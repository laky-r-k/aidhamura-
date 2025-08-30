from django.urls import path
from . import views

urlpatterns = [
    # URL for the main inbox page
    path('', views.chats, name='inbox'),
    
    # URL for a specific chat conversation page
    path('<str:username>/', views.chat_view, name='chat'),
    
    # Add this new URL to handle sending a message
    
]
