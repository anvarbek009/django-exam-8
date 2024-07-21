
from django.shortcuts import render,redirect,get_object_or_404
from .models import CategoryTransition, PaymentType,Transaction,CategoryThings
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TransactionForm, CategoryThingsForm,CategoryTransitionForm,PaymentTypeForm
from django.views import View
from django.contrib import messages
from django.db.models import Sum
# Create your views here.


class CategoryTransitionView(View):
    def get(self, request):
        category_transition = CategoryTransition.objects.all()
        return render(request, 'home.html', {"category_transition": category_transition})

class TransactionView(View):
    def get(self, request, pk):
        transaction = Transaction.objects.filter(category_transition_id=pk)
        return render(request, 'main/transaction_list.html', {"transaction": transaction})

class TransactionCreateView(View):
    def get(self, request):
        form = TransactionForm()
        return render(request, 'main/transaction_create.html', {'form': form})  
    def post(self, request):
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            if transaction.category_transition.name == 'Chiqim':
                payment_type = get_object_or_404(PaymentType, id=transaction.payment_type.id)
                payment_type.balance -= transaction.amount
                payment_type.save()
            elif transaction.category_transition.name == 'Kirim':
                payment_type = get_object_or_404(PaymentType, id=transaction.payment_type.id)
                payment_type.balance += transaction.amount
                payment_type.save()

            total_balance = PaymentType.objects.filter(user=request.user).aggregate(total=Sum('balance'))['total']

            messages.success(request, 'Transaction successfully created.')
            return redirect('main:wallet')
        else:
            return render(request, 'main/transaction_create.html', {'form': form})
        
class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        payment_types = PaymentType.objects.filter(user=request.user)
        balance = sum(payment_type.balance for payment_type in payment_types)
        return render(request, 'main/wallet.html', {"payment_types": payment_types, 'balance': balance})

class PaymentTypeCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = PaymentTypeForm(request.POST, request.FILES)
        if form.is_valid():
            payment_type = form.save(commit=False)
            payment_type.user = request.user
            payment_type.save()
            return redirect('wallet')
        else:
            return render(request, 'main/payment_type_create.html', {"form": form})
        

