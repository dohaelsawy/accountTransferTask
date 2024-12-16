# urls.py
from rest_framework.routers import DefaultRouter
from .views import ImportAccountsView, AccountManagementViewSet
from django.urls import path


router = DefaultRouter()
router.register(r'', AccountManagementViewSet,basename="accounts")

urlpatterns = [
    path('import_accounts/',ImportAccountsView.as_view(), name='import-accounts'),
] + router.urls