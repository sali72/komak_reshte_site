import csv
import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import FieldOfStudyForm
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
        field = _get_field_from_form(form)
        if _field_already_exists_in_list(field, request.session.get("field_list", [])):
            form.add_error("field_of_study", _("This item already exists in the list."))
            return _render_form_with_errors(request, form)
        if not _exam_group_consistent(field, request.session.get("field_list", [])):
            form.add_error(
                "exam_group",
                _("All items in the list must belong to the same exam group."),
            )
            return _render_form_with_errors(request, form)
        save_form_data_to_session(request, form)
        return redirect("komak_reshte:create_list")
    else:
        return _render_form_with_errors(request, form)


def _field_already_exists_in_list(field, field_list):
    return any(item["unique_code"] == field.unique_code for item in field_list)


def _exam_group_consistent(field, field_list):
    return all(item["exam_group"] == field.exam_group for item in field_list)


def save_form_data_to_session(request, form):
    field_list = request.session.get("field_list", [])
    field = _get_field_from_form(form)
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
    field_list.append(new_entry)
    for index, item in enumerate(field_list):
        item["order"] = index + 1
    request.session["field_list"] = field_list
    request.session.modified = True


def _get_field_from_form(form):
    field_id = form.cleaned_data["field_of_study"]
    return FieldOfStudy.objects.get(id=field_id)


def _render_form_with_errors(request, form):
    errors = form.errors
    for field, error_list in errors.items():
        for error_message in error_list:
            print(f"Error for field '{field}': {error_message}")
    context = {"form": form, "field_list": request.session["field_list"]}
    return render(request, "komak_reshte/create_list.html", context)


def render_create_list_form(request):
    form = FieldOfStudyForm()
    return render(
        request,
        "komak_reshte/create_list.html",
        {"form": form, "field_list": request.session["field_list"]},
    )


def get_fields_of_study(request):
    search_term = request.GET.get("q", "").strip()
    province = request.GET.get("province", None)
    exam_group = request.GET.get("exam_group", None)
    fields_of_study = get_filtered_fields_of_study(province, exam_group, search_term)
    response_data = [
        {
            "id": field["id"],
            "name": field["name"],
            "university": field["university__name"],
            "unique_code": field["unique_code"],
        }
        for field in fields_of_study
    ]
    return JsonResponse({"results": response_data})


def get_filtered_fields_of_study(province, exam_group, search_term):
    if not exam_group:
        return FieldOfStudy.objects.none()
    query = FieldOfStudy.objects.filter(exam_group=exam_group)
    if province:
        universities = University.objects.filter(province=province)
        query = query.filter(university__in=universities)
    if search_term:
        query = query.filter(
            Q(name__icontains=search_term)
            | Q(university__name__icontains=search_term)
            | Q(unique_code__icontains=search_term)
        )
    return query.values("id", "name", "university__name", "unique_code")


def get_provinces(request):
    search_term = request.GET.get("q", "").strip()
    if search_term:
        provinces = (
            University.objects.filter(province__icontains=search_term)
            .values_list("province", flat=True)
            .distinct()
        )
    else:
        provinces = University.objects.values_list("province", flat=True).distinct()
    results = [{"id": province, "text": province} for province in provinces]
    return JsonResponse({"results": results})


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


def delete_item(request, field_of_study_id):
    if request.method == "POST":
        field_list = request.session.get("field_list", [])
        field_list = [
            item for item in field_list if item["field_of_study"] != field_of_study_id
        ]
        request.session["field_list"] = field_list
        request.session.modified = True
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def import_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if csv_file:
            try:
                data = csv_file.read().decode("latin-1").splitlines()
            except UnicodeDecodeError as e:
                return JsonResponse(
                    {"status": "error", "message": f"Unicode decode error: {str(e)}"},
                    status=400,
                )
            reader = csv.DictReader(data)
            fieldnames = [field.lower() for field in reader.fieldnames]
            missing_columns = validate_csv_columns(fieldnames)
            if missing_columns:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"Missing columns: {', '.join(missing_columns)}",
                    },
                    status=400,
                )
            try:
                import_data_from_csv(reader, fieldnames)
                redirect("komak_reshte:create_list")
                return JsonResponse({"status": "success"})
            except KeyError as e:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"Missing or incorrect column: {str(e)}",
                    },
                    status=400,
                )
            except Exception as e:
                return JsonResponse(
                    {"status": "error", "message": f"Unexpected error: {str(e)}"},
                    status=400,
                )
        return JsonResponse(
            {"status": "error", "message": "No file provided"}, status=400
        )
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=400
    )


def validate_csv_columns(fieldnames):
    required_columns = [
        "unique code",
        "field of study",
        "exam group",
        "university",
        "province",
        "requires exam",
        "tuition type",
        "first half acceptances",
        "second half acceptances",
        "women",
        "men",
        "extra information",
    ]
    missing_columns = [col for col in required_columns if col not in fieldnames]
    return missing_columns


def import_data_from_csv(reader, fieldnames):
    # Delete existing records
    EnrollmentData.objects.all().delete()
    FieldOfStudy.objects.all().delete()
    University.objects.all().delete()
    for row in reader:
        row = {field.lower(): value for field, value in row.items()}  # Make the row keys lowercase
        try:
            university, created = University.objects.get_or_create(
                name=row["university"], province=row["province"]
            )
            field_of_study = FieldOfStudy.objects.create(
                unique_code=row["unique code"],
                exam_group=row["exam group"],
                name=row["field of study"],
                university=university,
                requires_exam=row["requires exam"] == "TRUE",
                tuition_type=row["tuition type"],
            )
            EnrollmentData.objects.create(
                field_of_study=field_of_study,
                first_half_acceptances=int(row["first half acceptances"]),
                second_half_acceptances=int(row["second half acceptances"]),
                women=row["women"],
                men=row["men"],
                extra_information=row.get("extra information", ""),
            )
        except KeyError as e:
            raise KeyError(_("Missing or incorrect column in row: {row}. Error: {e}").format(row=row, e=e))



def export_csv(request):
    field_list = request.session.get("field_list", [])
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="field_list.csv"'
    writer = csv.writer(response)

    # Write the header
    writer.writerow(
        [
            "Order",
            "Unique Code",
            "Field of Study",
            "Exam Group",
            "University",
            "Requires Exam",
            "Tuition Type",
            "First Half Acceptances",
            "Second Half Acceptances",
            "Women",
            "Men",
            "Extra Information",
        ]
    )

    # Write the data rows
    for item in field_list:
        writer.writerow(
            [
                item["order"],
                item["unique_code"],
                item["name"],
                item["exam_group"],
                item["university"],
                item["requires_exam"],
                item["tuition_type"],
                item["first_half_acceptances"],
                item["second_half_acceptances"],
                item["women"],
                item["men"],
                item["extra_information"],
            ]
        )
    return response
