from django.urls import path

from . import views

app_name = "komak_reshte"
urlpatterns = [
    path("", views.create_list, name="create_list"),
    path("export_csv/", views.export_csv, name="export_csv"),
    path("get-fields-of-study/", views.get_fields_of_study, name="get_fields_of_study"),
]
