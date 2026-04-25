from django import forms
from .models import Plan, Task

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']