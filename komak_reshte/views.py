import csv

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .crud.forms import FieldOfStudyForm
from .models import EnrollmentData, FieldOfStudy, University

def create_list(request):
    if "field_list" not in request.session:
        request.session["field_list"] = []
    
    if request.method == "POST":
        form = FieldOfStudyForm(request.POST)

        if form.is_valid():
            selected_province = form.cleaned_data['province']
            field_list = request.session["field_list"]

            if selected_province == '':  # All provinces selected
                new_entries = [{
                    "field_of_study": entry.id,
                    "order": entry.order
                } for entry in FieldOfStudy.objects.all()]
            else:
                universities = University.objects.filter(province=selected_province)
                new_entries = [{
                    "field_of_study": entry.id,
                    "order": entry.order
                } for entry in FieldOfStudy.objects.filter(university__in=universities)]

            field_list.extend(new_entries)
            request.session["field_list"] = field_list
            request.session.modified = True
            return redirect("komak_reshte:create_list")
        else:
            errors = form.errors
            for field, error_list in errors.items():
                for error_message in error_list:
                    print(f"Error for field '{field}': {error_message}")
            context = {'form': form}
            return render(request, 'create_list.html', context)
    else:
        form = FieldOfStudyForm()

    # Render the template with the form and the field_list from the session
    return render(
        request,
        "create_list.html",
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
