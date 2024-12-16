# urls.py
from rest_framework.routers import DefaultRouter
from .views import ImportAccountsView, AccountManagement
from django.urls import path


router = DefaultRouter()
router.register(r'', AccountManagement,basename="accounts")

urlpatterns = [
    path('import_accounts/',ImportAccountsView.as_view(), name='import-accounts'),
] + router.urls