from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Layout, Submit
from crispy_forms.bootstrap import FormActions


class LoginForm(forms.Form):
    '''Form for user login'''

    username = forms.CharField(
        label='Username',
        max_length=50,
        widget=forms.TextInput(attrs={'autocomplete': 'username'})
    )
    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )

    helper = FormHelper()
    helper.form_id = 'login-form'
    helper.layout = Layout(
        Row('username'),
        Row('password'),
        FormActions(
            Submit('login', 'Log in'),
        )
    )


class SignupForm(forms.Form):
    '''Form for user signup'''

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
            }
        )
    )

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'username',
            }
        )
    )

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'first name',
            }
        )
    )

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'last name',
            }
        )
    )

    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        max_length=50,
        widget=forms.PasswordInput,
    )

    helper = FormHelper()
    helper.form_id = 'signup-form'
    helper.layout = Layout(
        Row('email'),
        Row('username'),
        Row('first_name'),
        Row('last_name'),
        Row('date_of_birth'),
        Row('password'),
        Row('password_confirm'),
        FormActions(
            Submit('signup', 'Sign up', css_class="btn-primary")
        )
    )
