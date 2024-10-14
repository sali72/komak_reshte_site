from django.urls import path

from . import views

app_name = "komak_reshte"
urlpatterns = [
    path('', views.create_list, name='create_list'),
    path('export_csv/', views.export_csv, name='export_csv'),
    
    # path("", views.IndexView.as_view(), name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]