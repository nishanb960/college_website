from django.contrib import admin
from .models import StudentProfile, Course, Faculty, Event, Gallery, Contact, Admission

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'phone', 'enrollment_date']
    search_fields = ['user__username', 'student_id']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'duration', 'fees']
    search_fields = ['code', 'name']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'qualification', 'email']
    search_fields = ['name', 'designation']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'venue', 'is_upcoming']
    list_filter = ['is_upcoming', 'date']
    search_fields = ['title']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']
    search_fields = ['title']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at']
    search_fields = ['name', 'email', 'subject']

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'course', 'email', 'status', 'applied_date']
    list_filter = ['status', 'course']
    search_fields = ['full_name', 'email']