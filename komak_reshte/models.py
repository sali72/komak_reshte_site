from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255)
    province = models.CharField(max_length=255)


class FieldOfStudy(models.Model):
    unique_code = models.IntegerField(unique=True)
    exam_group = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    requires_exam = models.BooleanField()
    tuition_type = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.unique_code)

class EnrollmentData(models.Model):
    field_of_study = models.OneToOneField(FieldOfStudy, on_delete=models.CASCADE)
    first_half_acceptances = models.IntegerField()
    second_half_acceptances = models.IntegerField()
    women = models.CharField(max_length=50)
    men = models.CharField(max_length=50)
    extra_information = models.TextField(null=True)
