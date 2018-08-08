from django.contrib import admin

from .models import Lab, LabTasks, Grades, GradesReport, Course, CourseTopic, Post



admin.site.register(Lab)

admin.site.register(LabTasks)

# admin.site.register(LabComments)

# admin.site.register(LabNotes)

admin.site.register(Grades)

admin.site.register(GradesReport)

admin.site.register(Course)

admin.site.register(CourseTopic)

admin.site.register(Post)
