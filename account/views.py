from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone # for adding transaction list
from .models import Account, Transaction

import csv
import codecs

# +++++++++++ upload csv file+++++++++++++++
from .forms import UploadFileForm

def upload_file(request,account_id):
    content = ""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            content = "" 
            file = request.FILES['file']
            csvfile = csv.DictReader(codecs.iterdecode(file, 'utf-8'))
            overwrite_transaction(csvfile,account_id)
            # account saving
            
    else:
        form = UploadFileForm()
    return render(request, 'account/upload.html', {'form': form,
                            'content':content,
                            'account_id':account_id})
def overwrite_transaction(csvfile,account_id):
    account = get_object_or_404(Account, pk=account_id)
    account.total = 0
    for a in account.transaction_set.all(): # delete old data
        a.delete()
    for row in csvfile: # save new data
        account.total = account.total + int(row['value'])
        account.transaction_set.create(detail=row['detail'],
                                        value=int(row['value']),
                                        date=row['date'])
    account.save()
  
# ---------- end upload csvfile -----------
theme = 'account/stylewhite.css'

class IndexView(generic.ListView):
    template_name = 'account/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'theme': theme})
        return context
    
    def get_queryset(self):
        return Account.objects.order_by('-account_name')[:5]

class DetailView(generic.DetailView):
    model = Account
    template_name = 'account/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update({'theme': theme})
        return context
    
def add_account(request):
    try:
        get_name = request.POST['account_name']
    except:
        error_msg = "Error !"
    else:
        if get_name.isalpha():
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
    return HttpResponseRedirect(reverse('account:index'))
    
    
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
    #content = {'detail':get_detail,'value':get_value,'ttype':get_ttype,'error_message':error_message,'account_id':account_id}
    #return render(request, 'account/addtrans.html', content)
    return HttpResponseRedirect(reverse('account:detail', args=(account_id,)))
    
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
    
def export_csv(request,account_id):
    account = get_object_or_404(Account, pk=account_id)
    response = HttpResponse(content_type='text/csv')
    filename = account.account_name + "_data.csv"
    response['Content-Disposition'] = "attachment; filename="+filename
    writer = csv.DictWriter(response,fieldnames=['date','detail','value'])
    writer.writeheader()
    for a in account.transaction_set.all().values():
        detail = str(a['detail'])
        date = str(a['date'])
        value = str(a['value'])
        writer.writerow({'date': date, 'detail': detail,'value':value})
    return response

def switch(request):
    global theme
    if theme == 'account/stylewhite.css':
        theme = 'account/style.css'
    else:
        theme = 'account/stylewhite.css'
    return HttpResponseRedirect(reverse('account:index'))
    
