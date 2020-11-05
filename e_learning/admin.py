from django.contrib import admin
from e_learning.models import Lecture, Assignment, Major, Professor, OpenLecture, Language

admin.site.register(Assignment)
admin.site.register(Major)
admin.site.register(Language)

class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 0

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'major')
    fields = ['first_name', 'last_name', 'date_of_birth', 'major']
    inlines = [LectureInline]

class OpenLectureInline(admin.TabularInline):
    model = OpenLecture
    extra = 0

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'professor', 'major', 'language')
    inlines = [OpenLectureInline]

@admin.register(OpenLecture)
class OpenLectureAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'status', 'enroll_student', 'remain_time', 'id')
    list_filter = ('status', 'remain_time')

    fieldsets = (
        (None, {
            'fields': ('lecture', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'remain_time', 'enroll_student')
        }),
    )
