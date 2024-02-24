from django import forms
# from .models import Inquiry
#
# class InquiryForm(forms.ModelForm):
#     class Meta:
#         model = Inquiry
#         fields = ['first_name', 'last_name', 'email', 'phone', 'country', 'inquiry_note']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.fields['last_name'].required = True
#         self.fields['email'].required = True
#         self.fields['phone'].required = True