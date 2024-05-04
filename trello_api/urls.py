from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserCreate.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserUpdate.as_view(), name='user-put-patch'),
    path('columns/', views.ColumnCreate.as_view(), name='column-list'),
    path('columns/<int:pk>/', views.ColumnUpdate.as_view(), name='column-put-patch'),
    path('cards/', views.CardCreate.as_view(), name='card-list'),
    path('cards/<int:pk>/', views.CardUpdate.as_view(), name='card-put-patch'),
    path('cards/<int:pk>/', views.CardUpdate.as_view(), name='card-put-patch'),
    path('get/Column/<int:id>/', views.getColumnWithCardBasedOnUser,name="getColumnWithCardBasedOnUser"),
    path('getby/column/<int:id>/', views.getCardBasedOnColumn,name="getColumnWithCardBasedOnUser"),
    path('login/', views.UserLoginAPIView.as_view(),name="login"),
    path('columns/<int:column_id>/reorder/', views.reorder_cards_in_column, name='reorder_cards_in_column'),


]
