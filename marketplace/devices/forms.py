from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']

    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=1000,
        help_text='Максимальная длина: 1000 символов',
    )

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        help_text='Рейтинг: от 1 (плохо) до 5 (отлично)',
    )


class ReviewSearchForm(forms.Form):
    search_word = forms.CharField(help_text='Введите слово...', required=False)
