from django.urls import path
from . import views

urlpatterns = [
    path('clients_filter/', views.client_filter, name='client_filter'),
    path('equipments_filter/', views.equipment_filter, name='equipment_filter'),
    path('modes_filter/', views.mode_filter, name='mode_filter'),
    path('minutes_filter/', views.minute_filter, name='minute_filter'),
    path('start_date_filter/', views.start_date_filter, name='start_date_filter'),
    path('start_time_filter/', views.start_time_filter, name='start_time_filter'),
    path('end_date_filter/', views.end_date_filter, name='end_date_filter'),
    path('end_time_filter/', views.end_time_filter, name='end_time_filter'),
]
