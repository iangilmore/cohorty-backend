from django.contrib import admin
from .models import Course, StudentEnrollment, CourseStaff, Assignment, Submission, Attendance

# Register your models here.
admin.site.register(Course)
admin.site.register(StudentEnrollment)
admin.site.register(CourseStaff)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Attendance)