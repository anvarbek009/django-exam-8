from django.urls import path
from .views import CategoryTransitionView, WalletView, TransactionCreateView, TransactionView, PaymentTypeCreateView,TransactionNewestListView,TransactionUpdateView,PaymentTypeDeleteView,PaymentTypeUpdateView,StatisticsView

app_name = 'main'
urlpatterns = [
    path('', CategoryTransitionView.as_view(), name='home'),  
    path('wallet/', WalletView.as_view(), name='wallet'),      
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction_create'),  
    path('transaction/<int:pk>/', TransactionView.as_view(), name='transaction_list'),          
    path('payment_type/create/', PaymentTypeCreateView.as_view(), name='payment_type_create'), 
    path('transactions/newest/', TransactionNewestListView.as_view(), name='transaction_newest_list'),
    path('transaction/update/<int:pk>/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('payment_type/update/<int:pk>/', PaymentTypeUpdateView.as_view(), name='payment_type_update'),
    path('payment_type/delete/<int:pk>/', PaymentTypeDeleteView.as_view(), name='payment_type_delete'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]