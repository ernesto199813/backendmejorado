

from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('api.urls')), # Include your app URLs
    path('api/', include('calendario.urls')),
    path('api/', include('configuracion.urls')),
    path('api/', include('users.urls')),
    path('api/', include('formulario.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('classrooms.urls')),

]

