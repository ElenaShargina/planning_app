from django import forms
from .models import Plan, Task, FlashCard, FlashCardCollection, Timer, Bookmark


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
class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['title', 'url']
        widgets = {
            'bookmark_date': forms.DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'placeholder': 'Например: Учебник по алгебре'}),
            'url': forms.URLInput(attrs={'placeholder': 'https://...'})
        }
