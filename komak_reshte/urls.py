from django.urls import path

from . import views
from .views import delete_item

app_name = "komak_reshte"
urlpatterns = [
    path("", views.create_list, name="create_list"),
    path("export_csv/", views.export_csv, name="export_csv"),
    path("get-fields-of-study/", views.get_fields_of_study, name="get_fields_of_study"),
    path("update-order/", views.update_order, name="update_order"),
    path("delete_item/<int:field_of_study_id>/", delete_item, name="delete_item"),
    path("clear-list/", views.clear_list, name="clear_list"),
]
