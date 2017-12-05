from django.shortcuts import render

# Create your views here.
from rules.contrib.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django_pandas.io import read_frame
from chartjs.views.lines import BaseLineChartView
from .models import Measurement
import pandas as pd

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

class MeasurementDataView(LoginRequiredMixin, BaseLineChartView):
    fields = ['chest', 'abdomen', 'thigh', 'weight']
    obj = {}

    def get_context_data(self):
        self.prepare_data()
        return super(MeasurementDataView, self).get_context_data()

    def get_queryset(self):
        qset = Measurement.objects.filter(owner=self.request.user)
        return qset

    def get_labels(self):
        return self.obj['labels']

    def get_providers(self):
        fields = []
        for dataset in self.obj['datasets']:
            fields.append(dataset['label'])
        return fields

    def get_data(self):
        data = []
        for field in self.obj['datasets']:
            data.append(field['data'])
        return data

    def get_date_labels(self, start_date, end_date, freq):
        date_labels = pd.date_range(
                start_date,
                end_date,
                freq=freq
            )
        date_labels = date_labels.strftime('%Y-%b-%d').tolist()
        return date_labels

    def get_dataframe(self, labels_x=None):
        df = read_frame(
                self.get_queryset(),
                fieldnames=self.fields + ['created'] # TODO specify which fields to retrieve dynamically
            )

        df = df.drop_duplicates(subset='created', keep='last')
        df['created'] = df['created'].apply(
                lambda x: x.strftime('%Y-%b-%d')
            )

        if labels_x is not None:
            df = labels_x.merge(df, on='created', how='left')

        df = df.set_index('created')
        df = df.fillna("null")
        return df

    def prepare_data(self):
        labels_x = pd.DataFrame(
                self.get_date_labels(
                    datetime.now() - timedelta(weeks=4), # TODO specify look back period dynamically
                    datetime.now(),
                    freq='D'
                ),
                columns=['created']
            )

        df = self.get_dataframe(labels_x)

        self.obj['labels'] = df.index.tolist()
        self.obj['datasets'] = []

        for field in self.fields:
            self.obj['datasets'].append(
                {'label': field, 'data': []}
            )

        for field in self.obj['datasets']:
            field['data'] = df[field['label']].tolist()
