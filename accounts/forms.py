from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password']

    def clean(self):
        cleaned_data = super(userRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )
        
class userProfileForm(forms.ModelForm):
        address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...', 'required':'required'}))
        profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
        cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
        #ONE WAY OF MAKING THE FIELDS READ ONLY.
        # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
        # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

        class Meta:   
            model = UserProfile
            fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city',
                    'pin_code', 'latitude', 'longitude']
            
        #SECOND WAY OF MAKING THE FIELDS READ ONLY. BY WRITING THE INIT METHOD.
        def __init__(self, *args, **kwargs):
             super(userProfileForm, self).__init__(*args, **kwargs)
             for field in self.fields:
                  if field == 'latitude' or field == 'longitude':
                       self.fields[field].widget.attrs['readonly'] = 'readonly'