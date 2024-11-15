from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),  # Chat page
    path('response/', views.chatbot_response, name='chatbot_response'),  # Chatbot response API
]

# urlpatterns =[
#     path('', views.chat, name='chat'),  # Chat page
#     path('response/', views.chatbot_response, name='chatbot_response'),  # Chatbot response API
# ]
    
