
from django.shortcuts import render,redirect,get_object_or_404
from .models import CategoryTransition, PaymentType,Transaction,CategoryThings
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TransactionForm, CategoryThingsForm,CategoryTransitionForm,PaymentTypeForm
from django.views import View
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
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
        
class TransactionNewestListView(View):
    def get(self, request, *args, **kwargs):
        filter_value = request.GET.get('filter', '')

        if filter_value == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0)
            end_date = timezone.now()
        elif filter_value == 'this_week':
            start_date = timezone.now() - timedelta(days=timezone.now().weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0)
            end_date = timezone.now()
        elif filter_value == 'this_month':
            start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0)
            end_date = timezone.now()
        else:
            start_date = None
            end_date = None

        transactions = Transaction.objects.filter(user=request.user)
        if start_date and end_date:
            transactions = transactions.filter(date__range=[start_date, end_date])
        transactions = transactions.order_by('-date')

        return render(request, 'main/transaction_list_newest.html', {'transactions': transactions})

class TransactionUpdateView(View):
    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        form = TransactionForm(instance=transaction)
        return render(request, 'main/transaction_update.html', {'form': form, 'transaction': transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('main:transaction_list')
        return render(request, 'main/transaction_update.html', {'form': form, 'transaction': transaction})

    
class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        payment_types = PaymentType.objects.filter(user=request.user)
        balance = sum(payment_type.balance for payment_type in payment_types)
        return render(request, 'main/wallet.html', {"payment_types": payment_types, 'balance': balance})

class PaymentTypeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PaymentTypeForm()
        return render(request, 'main/payment_type_create.html', {"form": form})

    def post(self, request):
        form = PaymentTypeForm(request.POST, request.FILES)
        if form.is_valid():
            payment_type = form.save(commit=False)
            payment_type.user = request.user
            payment_type.save()
            return redirect('main:wallet')
        else:
            return render(request, 'main/payment_type_create.html', {"form": form})
        
class PaymentTypeUpdateView(View):
    def get(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk, user=request.user)
        form = PaymentTypeForm(instance=payment_type)
        return render(request, 'main/payment_type_update.html', {'form': form, 'payment_type': payment_type})

    def post(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk, user=request.user)
        form = PaymentTypeForm(request.POST, request.FILES, instance=payment_type)
        if form.is_valid():
            form.save()
            return redirect('main:wallet')
        return render(request, 'main/payment_type_update.html', {'form': form, 'payment_type': payment_type})

class PaymentTypeDeleteView(View):
    def post(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk, user=request.user)
        payment_type.delete()
        return redirect('main:wallet')
        

