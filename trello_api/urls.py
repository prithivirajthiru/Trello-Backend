from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreate.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserUpdate.as_view(), name='user-put-patch'),
    path('columns/', views.ColumnListCreate.as_view(), name='column-list'),
    path('columns/<int:pk>/', views.ColumnUpdate.as_view(), name='column-put-patch'),
    path('cards/', views.CardListCreate.as_view(), name='card-list'),
    path('cards/<int:pk>/', views.CardUpdate.as_view(), name='card-put-patch'),
    path('cards/<int:pk>/', views.CardUpdate.as_view(), name='card-put-patch'),
    path('get/Column/<int:id>/', views.getColumnWithCardBasedOnUser,name="getColumnWithCardBasedOnUser"),
    path('login/', views.UserLoginAPIView.as_view(),name="login"),

]
