from django.shortcuts import render

# Create your views here.
from rules.contrib.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
####TEST
import pdb
from datetime import datetime
from django_pandas.io import read_frame
import pandas as pd
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
        fields = ['chest', 'abdomen', 'thigh', 'weight', 'created']
        df = read_frame(qset, fieldnames=fields)
        fields.pop()
        df['created'] = df['created'].apply(lambda x: x.strftime('%Y-%b-%d'))
        df = df.drop_duplicates(subset='created') # TODO filter by age
        df = df.set_index('created')
        y = pd.DataFrame(self.get_date_range(), columns=['created'])
        y = y.set_index('created')
        df = pd.concat([y, df], axis=1)
        df = df.fillna("null")

        obj = {}
        obj['labels'] = df.index.tolist()
        obj['datasets'] = []

        for field in fields:
            obj['datasets'].append(
                {'label': field, 'data': []}
            )

        for field in obj['datasets']:
            field['data'] = df[field['label']].tolist()

        return HttpResponse(json.dumps(obj),
                            content_type='application/json')

    def get_date_range(self):
        dr = pd.date_range(
                datetime(2017, 11, 1, 0, 0, 0),
                datetime(2017, 11, 30, 0, 0, 0),
                freq='D'
            )
        dr = dr.strftime('%Y-%b-%d').tolist()
        return dr
