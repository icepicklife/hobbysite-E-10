from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Commission

class CommissionListView(ListView):

    model = Commission
    template_name = 'commission_listview.html'


class CommissionDetailView(DetailView):

    model = Commission
    template_name = 'commission_detailview.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by('-date_created_on')
        return context
    



# Create your views here.
