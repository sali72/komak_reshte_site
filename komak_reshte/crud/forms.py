from django import forms
from ..models import University, FieldOfStudy


class FieldOfStudyForm(forms.Form):
    @staticmethod
    def get_all_province_choices():
        all_provinces = University.objects.values_list("province", flat=True).distinct()
        province_choices = [("", "All")] + [
            (province, province) for province in all_provinces
        ]
        return province_choices

    @staticmethod
    def get_all_exam_group_choices():
        all_exam_groups = FieldOfStudy.objects.values_list(
            "exam_group", flat=True
        ).distinct()
        exam_group_choices = [("", "Select")] + [
            (exam_group, exam_group) for exam_group in all_exam_groups
        ]
        return exam_group_choices

    province = forms.ChoiceField(
        choices=[("", "All")],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    exam_group = forms.ChoiceField(
        choices=[("", "Select")],
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    field_of_study = forms.ChoiceField(
        choices=[("", "None")],
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        initial_data = kwargs.get("initial", {})
        super().__init__(*args, **kwargs)
        self.fields["province"].choices = self.get_all_province_choices()
        self.fields["exam_group"].choices = self.get_all_exam_group_choices()
        self.fields["province"].initial = initial_data.get("province", "")
        self.fields["exam_group"].initial = initial_data.get("exam_group", "")
        self.populate_fields_of_study()

    def populate_fields_of_study(self):
        selected_province = self.data.get("province") or self.initial.get("province")
        selected_exam_group = self.data.get("exam_group") or self.initial.get(
            "exam_group"
        )
        if selected_exam_group:
            if selected_province:
                fields_of_study = self.get_fields_of_study_for_province_and_exam_group(
                    selected_province, selected_exam_group
                )
            else:
                fields_of_study = self.get_fields_of_study_for_exam_group(
                    selected_exam_group
                )
        else:
            fields_of_study = [("", "None")]
        self.fields["field_of_study"].choices = fields_of_study

    def get_fields_of_study_for_province_and_exam_group(self, province, exam_group):
        universities = University.objects.filter(province=province)
        fields_of_study = FieldOfStudy.objects.filter(
            university__in=universities, exam_group=exam_group
        )
        return [("", "None")] + [
            (
                field.id,
                f"{field.name} - {field.university.name} (Code: {field.unique_code})",
            )
            for field in fields_of_study
        ]

    def get_fields_of_study_for_exam_group(self, exam_group):
        fields_of_study = FieldOfStudy.objects.filter(exam_group=exam_group)
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
