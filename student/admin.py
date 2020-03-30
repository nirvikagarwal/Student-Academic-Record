from django.contrib import admin
from student.models import *
# Register your models here.

admin.site.register(Department)
admin.site.register(AllSemester)
admin.site.register(AllSubject)
admin.site.register(StudentProfile)
admin.site.register(StudentMarks)
admin.site.register(StudentSubject)
admin.site.register(Cgpa)