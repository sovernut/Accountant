from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Account, Transaction

class IndexView(generic.ListView):
    template_name = 'account/index.html'

    def get_queryset(self):
        return Account.objects.order_by('-account_name')[:5]

class DetailView(generic.DetailView):
    model = Account
    template_name = 'account/detail.html'

def add_trans(request,account_id):
    detail = request.POST['detail']
    value = request.POST['value']
    ttype = request.POST['t_type']
    content = {'detail':detail,'value':value,'ttype':ttype}
    return render(request, 'account/addtrans.html', content)