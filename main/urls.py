from django.urls import path
from .views import home_page,WalletView

app_name = 'main'
urlpatterns = [
    path('', home_page, name='home'),
    path('wallet/', WalletView.as_view(), name='wallet'),
]