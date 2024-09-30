from django.contrib import admin
from django.contrib.admin import ModelAdmin,  StackedInline, TabularInline  # Import ModelAdmin and Inline classes

from .models import University, FieldOfStudy, EnrollmentData

class EnrollmentDataInline(TabularInline):
    model = EnrollmentData
    fk_name = 'field_of_study'

class FieldOfStudyAdmin(ModelAdmin):
    inlines = [EnrollmentDataInline]

admin.site.register(University)
admin.site.register(FieldOfStudy, FieldOfStudyAdmin)