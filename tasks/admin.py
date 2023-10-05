from django.contrib import admin
from .models import task_user, Task, Photo
from django.db.models import Case, When, IntegerField

# Register your models here.
class task_userAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password')


#task register in admin
class AdminPhotoInline(admin.TabularInline):
    model = Photo

class task_Admin(admin.ModelAdmin):
    inlines = [
        AdminPhotoInline,
    ]
    list_display = ('title', 'due_date', 'created_at', 'priority', 'user', 'completed')
    list_filter = ('created_at', 'due_date', 'priority', 'completed')
    search_fields = ('title',)
    ordering = (Case(
        When(priority='High', then=1),
        When(priority='Medium', then=2),
        When(priority='Low', then=3),
        default=4,
        output_field=IntegerField(),
    ),)

#photo register in admin
class photoAdmin(admin.ModelAdmin):
    list_display = ('task', 'image')



admin.site.register(task_user,task_userAdmin)
admin.site.register(Task, task_Admin)
admin.site.register(Photo, photoAdmin)



