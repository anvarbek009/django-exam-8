
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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from users.models import User
from django.urls import reverse
from django.http import JsonResponse
from datetime import datetime, timedelta

# Create your views here.


class CategoryTransitionView(View):
    def get(self, request):
        category_transition = CategoryTransition.objects.all()
        return render(request, 'home.html', {"category_transition": category_transition})


class TransactionView(View,LoginRequiredMixin):
    def get(self, request, pk):
        transaction = Transaction.objects.filter(user=request.user,category_transition_id=pk)

        return render(request, 'main/transaction_list.html', {"transaction": transaction})

class StatisticsView(View):
    def get(self, request):
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

        total_used = transactions.filter(category_transition__name='Chiqim').aggregate(Sum('amount'))['amount__sum'] or 0
        total_received = transactions.filter(category_transition__name='Kirim').aggregate(Sum('amount'))['amount__sum'] or 0

        return render(request, 'main/statistics.html', {
            'total_used': total_used,
            'total_received': total_received,
        })


@method_decorator(login_required, name='dispatch')
class TransactionCreateView(View):
    def get(self, request):
        form = TransactionForm(user=request.user)
        return render(request, 'main/transaction_create.html', {'form': form})

    def post(self, request):
        form = TransactionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            if transaction.category_transition.name == 'Chiqim':
                payment_type = get_object_or_404(PaymentType, id=transaction.payment_type.id, user=request.user)
                payment_type.balance -= transaction.amount
                payment_type.save()
            elif transaction.category_transition.name == 'Kirim':
                payment_type = get_object_or_404(PaymentType, id=transaction.payment_type.id, user=request.user)
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
        date_str = request.GET.get('date', '')

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
        elif date_str:
            try:
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                start_date = timezone.make_aware(datetime.combine(selected_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(selected_date, datetime.max.time()))
            except ValueError:
                start_date = end_date = None
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
        
@method_decorator(login_required, name='dispatch')
class SendMoneyView(View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        sender_payment_types = PaymentType.objects.filter(user=request.user)
        return render(request, 'main/send_money.html', {
            'users': users,
            'sender_payment_types': sender_payment_types
        })

    def post(self, request):
        recipient_username = request.POST.get('recipient')
        amount = int(request.POST.get('amount'))
        sender_payment_type_id = request.POST.get('sender_payment_type')
        recipient_payment_type_id = request.POST.get('recipient_payment_type')

        try:
            recipient = User.objects.get(username=recipient_username)
            sender_payment_type = PaymentType.objects.get(id=sender_payment_type_id, user=request.user)
            recipient_payment_type = PaymentType.objects.get(id=recipient_payment_type_id, user=recipient)
            
            if sender_payment_type.balance < amount:
                messages.error(request, "Insufficient balance.")
                return redirect('main:send_money')
            
            sender_payment_type.balance -= amount
            recipient_payment_type.balance += amount
            sender_payment_type.save()
            recipient_payment_type.save()
            
            messages.success(request, "Money sent successfully.")
            return redirect('main:home')
        
        except User.DoesNotExist:
            messages.error(request, "Recipient not found.")
            return redirect('main:send_money')
        except PaymentType.DoesNotExist:
            messages.error(request, "Invalid payment type selected.")
            return redirect('main:send_money')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('main:send_money')
        

@login_required
def get_payment_types(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
        payment_types = PaymentType.objects.filter(user=user)
        data = [{'id': pt.id, 'name': pt.name, 'balance': pt.balance} for pt in payment_types]
        return JsonResponse({'payment_types': data})
    except User.DoesNotExist:
        return JsonResponse({'payment_types': []})

