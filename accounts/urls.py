# urls.py
from rest_framework.routers import DefaultRouter
from .views import AccountManagementViewSet
from django.urls import path


router = DefaultRouter()
router.register(r'', AccountManagementViewSet,basename="accounts")

urlpatterns = [] + router.urls