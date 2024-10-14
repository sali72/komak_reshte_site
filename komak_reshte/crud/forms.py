from django import forms
from ..models import University, FieldOfStudy, EnrollmentData

class FieldOfStudyForm(forms.Form):
    all_provinces = University.objects.values_list('province', flat=True).distinct()
    province_choices = [('', 'All')] + [(province, province) for province in all_provinces]
    province = forms.ChoiceField(choices=province_choices, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        selected_province = self.data.get('province', None)
        if selected_province:
            universities = University.objects.filter(province=selected_province)
            fields_of_study = FieldOfStudy.objects.filter(university__in=universities)
            self.fields['field_of_study'].choices = [('', 'None')] + [(field.id, field.name) for field in fields_of_study]

    all_field_of_study = FieldOfStudy.objects.all()
    choices = [('', 'None')] + [(id, id) for id in all_field_of_study]
    field_of_study = forms.ChoiceField(choices=choices, required=True, widget=forms.Select())
    order = forms.IntegerField()
    