from django import forms
from .models import Plan, Task, FlashCard, FlashCardCollection, Timer


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']


class FlashCardCollectionForm(forms.ModelForm):
    class Meta:
        model = FlashCardCollection
        fields = ['title']


class FlashCardForm(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = ['title', 'front_side', 'back_side']


class TimerForm(forms.ModelForm):
    class Meta:
        model = Timer
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter timer title...', 'class': 'timer-input'}
            )
        }
