from datetime import date
from django import forms
import re
class RegistrationForm(forms.Form):
    fname = forms.CharField(label='First Name', max_length=100)
    lname = forms.CharField(label='Last Name', max_length=100)
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    repassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('fname')
        if not first_name.replace(" ", "").isalpha():
            raise forms.ValidationError("First Name should only contain letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('lname')
        if not last_name.replace(" ", "").isalpha():
            raise forms.ValidationError("Last Name should only contain letters")
        return last_name

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return date_of_birth

    def clean_password(self):
        password = self.cleaned_data.get('password')   
        # Check if password meets complexity requirements
        if len(password) < 5:
            raise forms.ValidationError("Password should be at least 5 characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password should contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password should contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password should contain at least one number.")
        if not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'",.<>?`~|]', password):
            raise forms.ValidationError("Password should contain at least one special character.")
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Please enter a valid email address.")
        return email
    

    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')

        if password and repassword and password != repassword:
            raise forms.ValidationError("Passwords do not match.")
        return repassword

