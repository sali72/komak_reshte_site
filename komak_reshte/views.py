import csv

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import EnrollmentData, FieldOfStudy, University
from .crud.forms import FieldOfStudyForm


def create_list(request):
    if "field_list" not in request.session:
        request.session["field_list"] = []

    if request.method == "POST":
        form = FieldOfStudyForm(request.POST)

        if form.is_valid():
            field_list = request.session["field_list"]

            new_entry = {
                "field_of_study": form.cleaned_data["field_of_study"],
                "order": form.cleaned_data["order"],
            }

            field_list.append(new_entry)

            request.session["field_list"] = field_list
            request.session.modified = True
            print(request.session["field_list"])
            return redirect("komak_reshte:create_list")
        else:
            errors = form.errors
            for field, error_list in errors.items():
                for error_message in error_list:
                    print(f"Error for field '{field}': {error_message}")
            context = {"form": form}
            print(request.session["field_list"])
            return render(request, "komak_reshte/create_list.html", context)
    else:
        form = FieldOfStudyForm()

    print(request.session["field_list"])
    return render(
        request,
        "komak_reshte/create_list.html",
        {"form": form, "field_list": request.session["field_list"]},
    )
    



def export_csv(request):
    field_list = request.session.get("field_list", [])
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="field_list.csv"'

    writer = csv.writer(response)
    writer.writerow(["Field of Study", "Order"])

    for item in field_list:
        writer.writerow([item["field_of_study"], item["order"]])

    return response
