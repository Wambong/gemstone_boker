from django import forms
from .models import ReviewRating, Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

class ProducteditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

