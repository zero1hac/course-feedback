from django.contrib import admin
from feedback.models import *

admin.site.register(Feedback)

admin.site.register(Faculty)
# Register your models here.

admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Courses)