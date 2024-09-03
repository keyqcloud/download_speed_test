from django.urls import path
from . import views

urlpatterns = [
    path('download/<str:filename>/', views.serve_file, name='serve_file'),
    path('download/stream/<str:filename>/', views.serve_file_stream, name='serve_file_stream'),
]

