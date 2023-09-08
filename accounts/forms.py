from django import forms
from .models import Account
import re


class RegisterForm(forms.ModelForm):

    password            =forms.CharField(min_length=8,widget=forms.PasswordInput(attrs={
                            'placeholder':'Enter Password',
                            'class':'form-control',
                            
                        }))

    confirm_password    =forms.CharField(widget=forms.PasswordInput(attrs={
                            'placeholder':'Confirm Password',
                            'class':'form-control',
                        }))
 

    email               =forms.CharField(widget=forms.EmailInput(attrs={
                            'placeholder':'Enter Email',
                            'class':'form-control'
                        }))
    
    confirm_email       =forms.CharField(widget=forms.EmailInput(attrs={
                            'placeholder':'Cofirm Email',
                            'class':'form-control'
                        }))

    class Meta:
        model   =Account
        fields  =['first_name', 'last_name', 'phone','password','email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm,self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder']   ='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']    ='Enter Last Name'
        self.fields['phone'].widget.attrs['placeholder']        ='Enter Phone Number'


        for field in self.fields:
            self.fields[field].widget.attrs['class']             ='form-control'

    
    def clean(self):
       
        cleaned_data=super(RegisterForm,self).clean()

        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        email=cleaned_data.get('email')
        confirm_email=cleaned_data.get('confirm_email')

        if password != confirm_password:
            super().add_error('password','Password must be matches!')

        if email !=confirm_email:
            super().add_error('email','Email must be matches!')

        # password validation
        if re.search('[a-z]',password) ==None:
            super().add_error('password','Password must have at least one lowercase character.')
        
        if re.search('[A-Z]',password) ==None:
            super().add_error('password','Password must have at least one Uppercase character.')
        
        if re.search('[0-9]',password) ==None:
            super().add_error('password','Password must have at least one digit .')
        
        if re.search('[!$@£%^&*()]',password) ==None:
            super().add_error('password','Password must have at least one psecial character [!$£%^&*()] .')

