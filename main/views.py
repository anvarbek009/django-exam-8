
from django.shortcuts import render,redirect
from .models import CategoryTransition, PaymentType,Transaction,CategoryThings
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TransactionForm, CategoryThingsForm,CategoryTransitionForm,PaymentTypeForm
from django.views import View
# Create your views here.


def home_page(request):
    return render(request, 'home.html')

class CategoryTransitionView(View):
    def get(self, request, pk):
        category_transition = CategoryTransition.objects.all()
        return render(request, 'home.html', {"category_transition": category_transition})

class TransactionView(View):
    def get(self, request, pk):
        transaction = Transaction.objects.filter(category_transaction=pk)
        return render(request, 'main/transaction_list.html', {"transaction": transaction})

class TransactionCreateView(View):
    def get(self, request, pk):
        form = TransactionForm()
        return render(request, 'main/transaction_create.html', {"form": form})

    def post(self, request, pk):
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.category_transition_id = pk
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list', pk=pk)
        return render(request, 'main/transaction_create.html', {"form": form})
 
class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        payment_types = PaymentType.objects.filter(user=request.user)
        balance = sum(payment_type.balance for payment_type in payment_types)
        return render(request, 'main/wallet.html', {"payment_types": payment_types, 'balance': balance})

class PaymentTypeCreateView(View):
    def post(self, request):
        form = PaymentTypeForm(request.POST, request.FILES)
        if form.is_valid():
            payment_type = form.save(commit=False)
            payment_type.user_id = request.user.id
            payment_type.save()
            return redirect('wallet')
        else:
            return render(request, 'main/payment_type_create.html', {"form": form})
        

