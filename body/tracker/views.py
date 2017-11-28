from django.shortcuts import render

# Create your views here.
from rules.contrib.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Measurement

class MeasurementListView(LoginRequiredMixin, ListView):
    model = Measurement
    context_object_name = "measurements"

    def get_queryset(self):
        return Measurement.objects.filter(owner=self.request.user)

class MeasurementDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'tracker.change_measurement'
    model = Measurement

    def get_object(self, queryset=None):
        obj = super(MeasurementDetailView, self).get_object(queryset=None)
        obj.total = obj.chest + obj.abdomen + obj.thigh
        return obj

class MeasurementCreateView(LoginRequiredMixin, CreateView):
    model = Measurement
    fields = ['chest', 'abdomen', 'thigh']

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super(MeasurementCreateView, self).form_valid(form)

class MeasurementUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'tracker.delete_measurement'
    model = Measurement
    fields = ['chest', 'abdomen', 'thigh']

class MeasurementDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'tracker.delete_measurement'
    model = Measurement
    success_url = reverse_lazy('tracker:list')
