from dataclasses import field
from pyexpat import model
from tkinter import Widget
from turtle import mode
from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import ProductReview , UserAddressBook , Comment , CommentBlog
from django.contrib.auth.forms import PasswordResetForm , SetPasswordForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name' , 'last_name' , 'email' , 'username' , 'password1' , 'password2')


# search


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()


	
# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating' , 'recommend')


class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address', 'mobile' , 'status')


class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields = ('first_name' , 'last_name' , 'email' , 'username')





class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address', 'mobile' , 'status')



class BootstrapStyleMixin:
    field_names = None


    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.field_names:
            for fieldname in self.field_names:
                self.fields[fieldname].widget.attrs = {'class': 'form-control'}
        else:
            raise ValueError('The field_names must be set')

			

class MyPassResetForm(BootstrapStyleMixin , PasswordResetForm):
    field_names = ['email']


class MySetPassForm(BootstrapStyleMixin , SetPasswordForm):
    field_names = ['new_password1' , 'new_password2']




class CouponsApplyForm(forms.Form):
    code = forms.CharField()

# Add Comment

class AddComment(forms.ModelForm):
	class Meta:
		model=Comment
		fields=('name','family' , 'email' , 'text_comment')


class CommentBlogForm(forms.ModelForm):
    class Meta:
        model = CommentBlog
        fields=('name' , 'title' ,'text',)