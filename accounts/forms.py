from django import forms
from .models import Account
class RegistrationForms(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter passsword',
                                                                'class':'form-controll'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',                                                                     'class':'form-control'}))
    class Meta:
        model = Account
        fields= ['first_name','last_name','phone_number','email','password']
    def __init__(self,*args,**kargs):
        super(RegistrationForms, self).__init__(*args,**kargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'phone number'
        for feild in self.fields:
            self.fields[feild].widget.attrs['class']='form-control'
    #password checking
    def clean(self):
        super(RegistrationForms, self).clean()
        password= self.cleaned_data.get('password')
        confirm_password= self.cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError(
                'password not matching'
            )

