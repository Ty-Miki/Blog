from django import forms
from .models import Comment

class_name = "pt-3 pb-2 px-5 block w-full rounded-xl mt-0 border-0 border-b-2 appearance-none focus:outline-none focus:ring-0 focus:border-black border-gray-200"

class EmailPostForm(forms.Form):

    # Fields to send email.
    name = forms.CharField(max_length=25,
                           widget=forms.TextInput(attrs={
                               "class": class_name,
                               "placeholder": " "
                           }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": class_name,
        "placeholder": " "
    }))
    to = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": class_name,
        "placeholder": " "
    }))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={
                                   "class": class_name,
                                   "placeholder": " "
                               }))
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            "name": forms.TextInput(attrs={"class": class_name, "placeholder": " "}),
            "email": forms.EmailInput(attrs={"class": class_name, "placeholder": " "}),
            "body": forms.Textarea(attrs={"class": class_name, "placeholder": " "})
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=25,
                           widget=forms.TextInput(attrs={
                               "class": class_name,
                               "placeholder": " "
                           }))