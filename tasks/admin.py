from django.contrib import admin
from django.utils import timezone
from .models import Plan, Task, FlashCardCollection, FlashCard


class TaskInline(admin.TabularInline):
    """Allow managing tasks directly from the Plan edit page."""
    model = Task
    extra = 1
    fields = ('title', 'description', 'status', 'created_at', 'completed_at')
    readonly_fields = ('created_at', 'completed_at')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'task_count')
    list_filter = ('user',)
    search_fields = ('title', 'description')
    inlines = [TaskInline]
    ordering = ('-id',)

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Total Tasks'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'plan', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'plan__user', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'completed_at')
    list_editable = ('status',)  # Change status directly from list view
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        """Auto-set/clear completed_at when status changes in admin."""
        if obj.status == 'completed' and not obj.completed_at:
            obj.completed_at = timezone.now()
        elif obj.status != 'completed':
            obj.completed_at = None
        super().save_model(request, obj, form, change)

@admin.register(FlashCardCollection)
class FlashCardCollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    list_filter = ('user',)
    search_fields = ('title',)

@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'collection')
    list_filter = ('collection__user',)
    search_fields = ('title', 'front_side', 'back_side')