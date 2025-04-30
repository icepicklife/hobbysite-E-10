from django.urls import path
from .views import CommissionDetailView, CommissionListView, CommissionCreateView, CommissionUpdateView

urlpatterns = [
    path("commissions/list", CommissionListView.as_view(),
         name="commission-list"),
    path(
        "commissions/detail/<int:pk>",
        CommissionDetailView.as_view(),
        name="commission-detail",
    ),
    path(
        "add",
        CommissionCreateView.as_view(),
        name='commission-add',
    ),
    path(
        "<int:pk>/edit",
        CommissionUpdateView.as_view(),
        name='commission-edit'
    )
]

app_name = "commission"
