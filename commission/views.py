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


class CommissionListView(LoginRequiredMixin, ListView):
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

class CommissionDetailView(LoginRequiredMixin, DetailView): 
    model = Commission
    template_name = 'commission_detailview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.get_object()
        jobs = commission.job_set.all()
        user = self.request.user
        profile = None

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)

        manpower_info = []
        total_required = 0
        total_open = 0

        for job in jobs:
            open_slots = job.manpower_required - job.jobapplication_set.filter(status='Accepted').count()
            already_applied = job.jobapplication_set.filter(applicant=profile).exists()
            can_apply = open_slots > 0 and not already_applied
            manpower_info.append((job, open_slots, can_apply))
            total_required += job.manpower_required
            total_open += open_slots

        context['manpower_info'] = manpower_info
        context['total_required'] = total_required
        context['total_open'] = total_open
        context['application_form'] = JobApplicationForm()
        context['is_owner'] = profile == commission.author if profile else False

        if context['is_owner']:
            applications = JobApplication.objects.filter(job__commission=commission).select_related('job', 'applicant')
            context['applications'] = applications

        return context


    def post(self, request, *args, **kwargs):
        commission = self.get_object()
        profile = get_object_or_404(Profile, user=request.user)

        # Owner accepting/rejecting
        if profile == commission.author:
            application_id = request.POST.get('application_id')
            action = request.POST.get('action')
            application = get_object_or_404(JobApplication, pk=application_id, job__commission=commission)

            if action == 'accept':
                application.status = 'Accepted'
                application.save()
            elif action == 'reject':
                application.status = 'Rejected'
                application.save()

            return redirect('commission:commission_detail', pk=commission.pk)

        # Applicant applying
        job_id = request.POST.get('job_id')
        job = get_object_or_404(Job, pk=job_id)

        existing_application = JobApplication.objects.filter(job=job, applicant=profile).first()

        if not existing_application:
            JobApplication.objects.create(
                job=job,
                applicant=profile,
                status='Pending',
                applied_on=timezone.now()
            )
            # ✅ Optional: add a message.success here
        else:
            # ✅ Optional: message.warning('You already applied')
            pass

        return redirect('commission:commission_detail', pk=commission.pk)


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