from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum, Case, When, Value, IntegerField

from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobFormSet, JobApplicationForm
from user_management.models import Profile

class CommissionListView(ListView):
    model = Commission
    template_name = 'commission_listview.html'
    context_object_name = 'commissions'

    def get_queryset(self):
        status_order = Case(
            When(status='Open', then=Value(0)),
            When(status='Full', then=Value(1)),
            When(status='Completed', then=Value(2)),
            When(status='Discontinued', then=Value(3)),
            output_field=IntegerField()
        )
        return Commission.objects.annotate(
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
    template_name = 'commission_detailview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        jobs = commission.job_set.all()
        profile = None

        if profile == commission.author:
            applications = JobApplication.objects.filter(job__commission=commission).select_related('applicant', 'job')
            context['applications'] = applications

        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

        manpower_info = []
        total_required = 0
        total_open = 0

        for job in jobs:
            accepted_count = job.jobapplication_set.filter(status='Accepted').count()
            open_slots = max(job.manpower_required - accepted_count, 0)
            can_apply = (
                profile and job.status == 'Open' and open_slots > 0 and
                not job.jobapplication_set.filter(applicant=profile).exists()
            )
            manpower_info.append((job, open_slots, can_apply))
            total_required += job.manpower_required
            total_open += open_slots

        context['manpower_info'] = manpower_info
        context['total_required'] = total_required
        context['total_open'] = total_open
        context['application_form'] = JobApplicationForm()
        context['is_owner'] = profile == commission.author if profile else False

        return context

    def post(self, request, *args, **kwargs):

        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, pk=job_id)
        profile = get_object_or_404(Profile, user=request.user)
        form = JobApplicationForm(request.POST)

        # Prevent applying if job is full
        accepted_count = job.jobapplication_set.filter(status='Accepted').count()
        if job.status == 'Full' or accepted_count >= job.manpower_required:
            messages.error(request, "This job is already full. Cannot apply.")
            return redirect('commission:commission_detail', pk=job.commission.id)

        # Prevent duplicate application
        if job.jobapplication_set.filter(applicant=profile).exists():
            messages.error(request, "You have already applied for this job.")
            return redirect('commission:commission_detail', pk=job.commission.id)

        if form.is_valid():
            job_app = form.save(commit=False)
            job_app.job = job
            job_app.applicant = profile
            job_app.applied_on = timezone.now()
            job_app.save()
            messages.success(request, "Application submitted successfully.")

        return redirect('commission:commission_detail', pk=job.commission.id)

class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commission_form.html'
    success_url = reverse_lazy('commission:commission_list')

    def get(self, request, *args, **kwargs):
        form = CommissionForm()
        formset = JobFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = CommissionForm(request.POST)
        formset = JobFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            commission = form.save(commit=False)
            commission.author = get_object_or_404(Profile, user=request.user)
            commission.created_on = timezone.now()
            commission.updated_on = timezone.now()
            commission.save()

            jobs = formset.save(commit=False)
            for job in jobs:
                job.commission = commission
                job.save()

            return redirect('commission:commission_list')

        return render(request, self.template_name, {'form': form, 'formset': formset})

class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commission_form.html'
    success_url = reverse_lazy('commission:commission_list')

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Commission.objects.filter(author=profile)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = JobFormSet(instance=self.object)
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = JobFormSet(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            commission = form.save(commit=False)
            commission.updated_on = timezone.now()
            commission.save()
            formset.save()

            if all(job.status == 'Full' for job in commission.job_set.all()):
                commission.status = 'Full'
                commission.save()

            return redirect(self.get_success_url())

        return render(request, self.template_name, {'form': form, 'formset': formset})


class JobApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = JobApplication
    form_class = JobApplication
    template_name = 'job_application_form.html'
    success_url = reverse_lazy('commission:commission_list')

    def dispatch(self, request, *args, **kwargs):
        app = self.get_object()
        if app.job.commission.author.user != request.user:
            return HttpResponseForbidden("You are not allowed to evaluate this application.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        job = self.object.job
        accepted_count = job.jobapplication_set.filter(status='Accepted').count()

        if accepted_count >= job.manpower_required:
            job.status = 'Full'
            job.save()
        else:
            if job.status != 'Open':
                job.status = 'Open'
                job.save()

        commission = job.commission
        if all(j.status == 'Full' for j in commission.job_set.all()):
            commission.status = 'Full'
            commission.save()
        else:
            if commission.status == 'Full':
                commission.status = 'Open'
                commission.save()

        messages.success(self.request, "Application has been updated and statuses auto-checked.")
        return response