from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Commission

class CommissionListView(ListView):

    model = Commission
    template_name = 'commission_listview.html'


class CommissionDetailView(DetailView):

    model = Commission
    template_name = 'commission_detailview.html'
    



# Create your views here.
