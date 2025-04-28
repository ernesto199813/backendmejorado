from django.urls import path
from .views import ClassroomListCreateView, ClassroomDetailView

urlpatterns = [
    path('classrooms/', ClassroomListCreateView.as_view(), name='classroom-list-create'),
    path('classrooms/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),
]