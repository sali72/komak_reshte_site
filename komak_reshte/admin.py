from django.contrib import admin

from .models import University, FieldOfStudy, EnrollmentData


admin.site.register(University, FieldOfStudy)
