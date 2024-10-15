import csv
import json

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
    field_list = request.session.get("field_list", [])

    # Fetch the actual FieldOfStudy object
    field_id = form.cleaned_data["field_of_study"]
    field = FieldOfStudy.objects.get(id=field_id)

    new_entry = {
        "field_of_study": field.id,
        "unique_code": field.unique_code,
        "name": field.name,
        "exam_group": field.exam_group,
        "university": field.university.name,
        "requires_exam": field.requires_exam,
        "tuition_type": field.tuition_type,
        "first_half_acceptances": field.enrollmentdata.first_half_acceptances,
        "second_half_acceptances": field.enrollmentdata.second_half_acceptances,
        "women": field.enrollmentdata.women,
        "men": field.enrollmentdata.men,
        "extra_information": field.enrollmentdata.extra_information,
    }

    # Append new entry
    field_list.append(new_entry)

    # Reorder list
    for index, item in enumerate(field_list):
        item["order"] = index + 1

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


def update_order(request):
    if request.method == "POST":
        ordered_data = _get_ordered_data_from_request(request)
        field_list = _get_field_list_from_session(request)

        field_dict = _create_field_dict(field_list)
        new_field_list = _update_field_list_order(ordered_data, field_dict)

        _save_field_list_to_session(request, new_field_list)
        return JsonResponse({"message": "Order updated successfully"})

    return JsonResponse({"message": "Invalid request method"}, status=400)


def _get_ordered_data_from_request(request):
    return json.loads(request.POST.get("ordered_data", "[]"))


def _get_field_list_from_session(request):
    return request.session.get("field_list", [])


def _create_field_dict(field_list):
    return {str(item["field_of_study"]): item for item in field_list}


def _update_field_list_order(ordered_data, field_dict):
    new_field_list = []
    for order, field_id in enumerate(ordered_data, start=1):
        field_id = str(field_id)
        if field_id in field_dict:
            field_dict[field_id]["order"] = order
            new_field_list.append(field_dict[field_id])
    return new_field_list


def _save_field_list_to_session(request, new_field_list):
    request.session["field_list"] = new_field_list
    request.session.modified = True


def export_csv(request):
    field_list = request.session.get("field_list", [])
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="field_list.csv"'

    writer = csv.writer(response)
    writer.writerow(["Field of Study", "Order"])

    for item in field_list:
        writer.writerow([item["field_of_study"], item["order"]])

    return response
