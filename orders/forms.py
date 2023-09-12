from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model= Order
        fields = ['first_name', 'last_name','phone', 'email', 'address_line_1', 'address_line_2','country', 'city','postcode','order_note']

    
    def __init__(self, *args, **kwargs):
        super(OrderForm,self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder']       ='First Name'
        self.fields['last_name'].widget.attrs['placeholder']        ='Last Name'
        self.fields['phone'].widget.attrs['placeholder']            ='Phone Number'
        self.fields['address_line_1'].widget.attrs['placeholder']    ='Addess Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder']    ='Addess Line 2'
        self.fields['country'].widget.attrs['placeholder']          ='Country'
        self.fields['city'].widget.attrs['placeholder']             ='City'
        self.fields['postcode'].widget.attrs['placeholder']             ='Post Code'
        self.fields['order_note'].widget.attrs['placeholder']             ='Please Write Your Note'


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    
    email=forms.CharField(widget=forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Email'
                }))

