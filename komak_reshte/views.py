import csv

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .crud.forms import FieldOfStudyForm
from .models import EnrollmentData, FieldOfStudy, University


def create_list(request):
    initialize_session_field_list(request)
    if request.method == "POST":
        return handle_post_request(request)
    return render_create_list_form(request)


def initialize_session_field_list(request):
    if "field_list" not in request.session:
        request.session["field_list"] = []


def handle_post_request(request):
    form = FieldOfStudyForm(request.POST)
    if form.is_valid():
        save_form_data_to_session(request, form)
        return redirect("komak_reshte:create_list")
    else:
        return render_form_with_errors(request, form)


def save_form_data_to_session(request, form):
    field_list = request.session["field_list"]
    new_entry = {
        "field_of_study": form.cleaned_data["field_of_study"],
        "order": len(field_list)
        + 1,  # Automatically set the order to the end of the list
    }
    field_list.append(new_entry)
    request.session["field_list"] = field_list
    request.session.modified = True


def render_form_with_errors(request, form):
    errors = form.errors
    for field, error_list in errors.items():
        for error_message in error_list:
            print(f"Error for field '{field}': {error_message}")
    context = {"form": form}
    return render(request, "komak_reshte/create_list.html", context)


def render_create_list_form(request):
    form = FieldOfStudyForm()
    return render(
        request,
        "komak_reshte/create_list.html",
        {"form": form, "field_list": request.session["field_list"]},
    )


def get_fields_of_study(request):
    province = request.GET.get("province", None)
    fields_of_study = get_filtered_fields_of_study(province)
    response_data = [
        {
            "id": field["id"],
            "name": field["name"],
            "university": field["university__name"],
            "unique_code": field["unique_code"],
        }
        for field in fields_of_study
    ]
    return JsonResponse({"fields_of_study": response_data})


def get_filtered_fields_of_study(province):
    if province:
        universities = University.objects.filter(province=province)
        fields_of_study = FieldOfStudy.objects.filter(
            university__in=universities
        ).values("id", "name", "university__name", "unique_code")
    else:
        fields_of_study = []
    return fields_of_study


def clear_list(request):
    if request.method == "POST":
        if "field_list" in request.session:
            del request.session["field_list"]
        request.session.modified = True
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def export_csv(request):
    field_list = request.session.get("field_list", [])
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="field_list.csv"'

    writer = csv.writer(response)
    writer.writerow(["Field of Study", "Order"])

    for item in field_list:
        writer.writerow([item["field_of_study"], item["order"]])

    return response
