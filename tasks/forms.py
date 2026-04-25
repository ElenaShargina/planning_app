from django import forms
from .models import Plan, Task, FlashCard, FlashCardCollection

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

# Add to the end
class FlashCardCollectionForm(forms.ModelForm):
    class Meta:
        model = FlashCardCollection
        fields = ['title']

class FlashCardForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = ['title', 'front_side', 'back_side']