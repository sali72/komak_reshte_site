from django import forms
from ..models import University, FieldOfStudy, EnrollmentData


class FieldOfStudyForm(forms.Form):
    all_provinces = University.objects.values_list("province", flat=True).distinct()
    province_choices = [("", "All")] + [
        (province, province) for province in all_provinces
    ]
    province = forms.ChoiceField(choices=province_choices, required=False)
    field_of_study = forms.ChoiceField(
        choices=[("", "None")], required=True, widget=forms.Select()
    )
    order = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.populate_fields_of_study()

    def populate_fields_of_study(self):
        selected_province = self.data.get("province", None)
        if selected_province:
            fields_of_study = self.get_fields_of_study_for_province(selected_province)
        else:
            fields_of_study = self.get_all_fields_of_study()
        self.fields["field_of_study"].choices = fields_of_study

    def get_fields_of_study_for_province(self, province):
        universities = University.objects.filter(province=province)
        fields_of_study = FieldOfStudy.objects.filter(university__in=universities)
        return [("", "None")] + [
            (
                field.id,
                f"{field.name} - {field.university.name} (Code: {field.unique_code})",
            )
            for field in fields_of_study
        ]

    def get_all_fields_of_study(self):
        all_field_of_study = FieldOfStudy.objects.all()
        return [("", "None")] + [
            (
                field.id,
                f"{field.name} - {field.university.name} (Code: {field.unique_code})",
            )
            for field in all_field_of_study
        ]
