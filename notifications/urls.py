from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.NotificationListCreateView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/<int:pk>/mark-as-read/', views.MarkAsReadView.as_view(), name='notification-mark-as-read'),
]