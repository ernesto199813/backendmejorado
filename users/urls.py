from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, UserView, UserProfileView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Ruta para obtener el token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Nueva ruta para refrescar el token
    path('users/', UserView.as_view(), name='user_list'),  # Ruta para la vista de usuarios
    path('users/me/', UserProfileView.as_view(), name='user_profile'),
]