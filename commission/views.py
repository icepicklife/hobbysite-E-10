from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobForm, JobApplicationForm
from user_management.models import Profile

from django.utils import timezone
from django.db.models import Sum, Count, Case, When, Value, IntegerField


class CommissionListView(ListView):

    model = Commission
    template_name = 'commissions/commission_list.html'
    context_object_name = 'commissions'

    def get_queryset(self):

        status_order = Case(
            When(status='Open', then=Value(0)),
            When(status='Full', then=Value(1)),
            When(status='Completed', then=Value(2)),
            When(status='Discontinued', then=Value(3)),
            output_field=IntegerField()
        )

        return Commission.objects.all().annotate(
            status_order=status_order
        ).order_by('status_order', '-created_on')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)
            context['user_commissions'] = Commission.objects.filter(author=profile)
            context['applied_commissions'] = Commission.objects.filter(
                job__jobapplication__applicant=profile
            ).distinct()

        return context


class CommissionDetailView(DetailView):

    model = Commission
    template_name = 'commissions/commission_detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        jobs = commission.job_set.all()
        profile = None

        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        manpower_info = []
        for job in jobs:
            accepted_count = job.jobapplication_set.filter(status='Accepted').count()
            open_slots = max(job.manpower_required - accepted_count, 0)
            can_apply = (
                profile and job.status == 'Open' and accepted_count < job.manpower_required and
                not job.jobapplication_set.filter(applicant=profile).exists()
            )
            manpower_info.append((job, open_slots, can_apply))

        context['manpower_info'] = manpower_info
        context['application_form'] = JobApplicationForm()
        context['is_owner'] = profile == commission.author if profile else False

        return context

    def post(self, request, *args, **kwargs):

        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, pk=job_id)
        profile = get_object_or_404(Profile, user=request.user)
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            job_app = form.save(commit=False)
            job_app.job = job
            job_app.applicant = profile
            job_app.applied_on = timezone.now()
            job_app.save()
        return redirect('commission-detail', pk=job.commission.id)


class CommissionCreateView(LoginRequiredMixin, CreateView):

    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_form.html'
    success_url = reverse_lazy('commission-list')

    def form_valid(self, form):

        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.author = profile
        form.instance.created_on = timezone.now()
        form.instance.updated_on = timezone.now()
        return super().form_valid(form)


class CommissionUpdateView(LoginRequiredMixin, UpdateView):

    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/commission_form.html'
    success_url = reverse_lazy('commission-list')

    def form_valid(self, form):

        form.instance.updated_on = timezone.now()
        response = super().form_valid(form)

        # Check if all jobs are Full
        all_full = all(job.status == 'Full' for job in self.object.job_set.all())
        if all_full:
            self.object.status = 'Full'
            self.object.save()

        return response

    def get_queryset(self):

        profile = get_object_or_404(Profile, user=self.request.user)
        
        return Commission.objects.filter(author=profile)