from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone # for adding transaction list
from .models import Account, Transaction

class IndexView(generic.ListView):
    template_name = 'account/index.html'

    def get_queryset(self):
        return Account.objects.order_by('-account_name')[:5]

class DetailView(generic.DetailView):
    model = Account
    template_name = 'account/detail.html'

def add_account(request):
    try:
        get_name = request.POST['account_name']
    except:
        error_msg = "Error !"
    else:
        a = Account(account_name=get_name,total=0)
        a.save()
    return HttpResponseRedirect(reverse('account:index'))

def del_account(request):
    error_msg = ""
    try:
        get_id = request.POST['account_id']
    except:
        error_msg = "You didn't select any account !"
    else:
        a = Account.objects.get(id=get_id)
        a.delete()
    account_list = Account.objects.order_by('-account_name')[:5]
    return render(request,'account/index.html',{'account_list':account_list,'error_msg':error_msg})    
    
def add_trans(request,account_id):
    account = get_object_or_404(Account, pk=account_id)
    error_message = 0
    try:
        get_detail = request.POST['detail']
        get_value = int(request.POST['value'])
        get_ttype = request.POST['t_type']
    except:
        get_detail = "None"
        get_value = "None"
        get_ttype = "None"
        error_message = 1
    else:
        if get_ttype == 'expense':
            get_value = -1*get_value
        account.total = account.total + get_value
        account.save()
        account.transaction_set.create(detail=get_detail,value=get_value,date=timezone.now())
    content = {'detail':get_detail,'value':get_value,'ttype':get_ttype,'error_message':error_message,'account_id':account_id}
    return render(request, 'account/addtrans.html', content)

def editname(request,account_id):
    account = get_object_or_404(Account, pk=account_id)
    try:
        get_name = request.POST['name']
    except:
        error = 1
    else:
        account.account_name = get_name
        account.save()
    return HttpResponseRedirect(reverse('account:detail', args=(account_id,)))