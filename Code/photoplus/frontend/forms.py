from django import forms
from captcha.fields import CaptchaField

#class ContactForm(forms.Form):
#    subject = forms.CharField()
#    email = forms.EmailField(required=False)
#    message = forms.CharField()


class ReCaptchaForm(forms.Form):
    subject = forms.CharField(
   	    max_length=70,
            label='Your subject')
    email = forms.EmailField(
	    min_length=4,
            label='Your e-mail address',
            #required=False,
            )
    message = forms.CharField(
	    max_length=1000,
	    min_length=0,
            label='Your message',
	    widget=forms.Textarea)
    captcha = CaptchaField(
            label= ("Captcha:")
            )

def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message
