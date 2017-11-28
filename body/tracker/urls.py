from django.conf.urls import url

from . import views

app_name = 'tracker'
urlpatterns = [
    # e.g. /tracker/
    url(
        r'^$',
        views.MeasurementListView.as_view(),
        name='list'
    ),

    # e.g. /tracker/5/
    url(
        r'^(?P<pk>[0-9]+)/$',
        views.MeasurementDetailView.as_view(),
        name='detail'
    ),

    #e.g. /tracker/new/
    url(
        r'^new/',
        views.MeasurementCreateView.as_view(),
        name='new'
    ),

    #e.g. /tracker/5/update
    url(
        r'^(?P<pk>[0-9]+)/update/$',
        views.MeasurementUpdateView.as_view(),
        name='update'
    ),

    #e.g. /tracker/5/delete
    url(
        r'^(?P<pk>[0-9]+)/delete/$',
        views.MeasurementDeleteView.as_view(),
        name='delete'
    ),
]
