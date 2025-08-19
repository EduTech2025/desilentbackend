from django.urls import path
from .views import ContactAPIView

urlpatterns = [
    path('email/', ContactAPIView.as_view(), name='contact_api'),
]
