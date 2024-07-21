from django.urls import path
from .views import CategoryTransitionView, WalletView, TransactionCreateView, TransactionView, PaymentTypeCreateView

app_name = 'main'
urlpatterns = [
    path('', CategoryTransitionView.as_view(), name='home'),  
    path('wallet/', WalletView.as_view(), name='wallet'),      
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction_create'),  
    path('transaction/<int:pk>/', TransactionView.as_view(), name='transaction_list'),          
    path('payment_type/create/', PaymentTypeCreateView.as_view(), name='payment_type_create'), 
]