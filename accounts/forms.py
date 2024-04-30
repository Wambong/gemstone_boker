from django import forms
from .models import Account, UserProfile, Testimony
from django.core.exceptions import ValidationError
from multiupload.fields import MultiFileField
from django_ckeditor_5.widgets import CKEditor5Widget
from store.models import Product


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter password"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm password"
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'customer_type', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('password and confirm password do not match! Try again')

        def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
            self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
            self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
            self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ("Image files only")},
                                       widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
class AccountUpdateForm(forms.ModelForm):
  class Meta:
    model = Account
    fields = ["phone_number", "is_admin", "customer_type", "is_staff", "is_active", "is_superadmin"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
                 'product_name', 'slug', 'description', 'price', 'images', 'stock', 'is_Available', 'category', 'country'
                ]
        widgets = {
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }



# forms.py


from store.models import Variation


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'variation_category', 'variation_value', 'is_active']


from store.models import ProductGallery


class ProductGalleryForm(forms.ModelForm):
    images = MultiFileField(min_num=1, max_num=20)

    class Meta:
        model = ProductGallery
        fields = ['product', 'images']





class TestimonyForm(forms.ModelForm):
  class Meta:
    model = Testimony
    fields = ['content']


