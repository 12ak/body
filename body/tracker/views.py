from django.shortcuts import render

# Create your views here.
from rules.contrib.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
####TEST
import pdb
import simplejson as json
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Measurement

class MeasurementListView(LoginRequiredMixin, ListView):
    model = Measurement
    context_object_name = "measurements"

    def get_queryset(self):
        qset =  Measurement.objects.filter(owner=self.request.user)
        qset = qset.extra(order_by = ['-created'])
        pdb.set_trace()
        return qset

class MeasurementDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'tracker.change_measurement'
    model = Measurement

class MeasurementCreateView(LoginRequiredMixin, CreateView):
    model = Measurement
    fields = ['chest', 'abdomen', 'thigh', 'weight']

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super(MeasurementCreateView, self).form_valid(form)

class MeasurementUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'tracker.delete_measurement'
    model = Measurement
    fields = ['chest', 'abdomen', 'thigh', 'weight']

class MeasurementDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'tracker.delete_measurement'
    model = Measurement
    success_url = reverse_lazy('tracker:list')

class MeasurementDataView(LoginRequiredMixin, TemplateView):
    def render_to_response(self, context):
        qset = Measurement.objects.filter(owner=self.request.user)
        fields = ['chest', 'abdomen', 'thigh', 'weight']
        obj = {}
        obj['labels'] = ["X", "Y", "Z"]
        obj['datasets'] = []

        for field in fields:
            obj['datasets'].append(
                {'label': field, 'data': []}
            )

        for measurement in qset:
            for field in obj['datasets']:
                field['data'].append(
                    getattr(measurement, field['label'])
                )

        return HttpResponse(json.dumps(obj))
