from django import forms
from captcha.fields import CaptchaField

class buyForm(forms.Form):
    FirstName = forms.CharField(
   	max_length=70,
        label='First Name')
    LastName = forms.CharField(
   	max_length=70,
        label='Last Name')
    Email = forms.EmailField(
	min_length=4,
        label='Your e-mail address',
        help_text='We will send your order confirmation here',
            )
    Country = forms.ChoiceField(
        label='Country',
 	choices=(
	('Abkhazia', 'Abkhazia'),
    	('Australia', 'Australia'),
    	('Austria', 'Austria'),
   	('Azerbaijan', 'Azerbaijan'),
    	('Albania', 'Albania'),
	('Angola', 'Angola'),
    	('Andorra', 'Andorra'),
    	('Argentina', 'Argentina'),
   	('Armenia', 'Armenia'),
    	('Bahamas', 'Bahamas'),
	 ('Bengali', 'Bengali'),
	 ('bs', 'Bosnian'),
	 ('ca', 'Catalan'),
	 ('cs', 'Czech'),
	 ('cy', 'Welsh'),
	 ('da', 'Danish'),
	 ('de', 'German'),
	 ('el', 'Greek'),
	 ('en', 'English'),
	 ('en-gb', 'British English'),
	 ('eo', 'Esperanto'),
	 ('es', 'Spanish'),
	 ('es-ar', 'Argentinian Spanish'),
	 ('es-mx', 'Mexican Spanish'),
	 ('es-ni', 'Nicaraguan Spanish'),
	 ('et', 'Estonian'),
	 ('eu', 'Basque'),
	 ('fa', 'Persian'),
	 ('fi', 'Finnish'),
	 ('fr', 'French'),
	 ('fy-nl', 'Frisian'),
	 ('ga', 'Irish'),
	 ('gl', 'Galician'),
	 ('he', 'Hebrew'),
	 ('hi', 'Hindi'),
	 ('hr', 'Croatian'),
	 ('hu', 'Hungarian'),
	 ('id', 'Indonesian'),
	 ('is', 'Icelandic'),
	 ('it', 'Italian'),
	 ('ja', 'Japanese'),
	 ('ka', 'Georgian'),
	 ('kk', 'Kazakh'),
	 ('km', 'Khmer'),
	 ('kn', 'Kannada'),
	 ('ko', 'Korean'),
	 ('lt', 'Lithuanian'),
	 ('lv', 'Latvian'),
	 ('mk', 'Macedonian'),
	 ('ml', 'Malayalam'),
	 ('mn', 'Mongolian'),
	 ('nb', 'Norwegian Bokmal'),
	 ('ne', 'Nepali'),
	 ('nl', 'Dutch'),
	 ('nn', 'Norwegian Nynorsk'),
	 ('pa', 'Punjabi'),
	 ('pl', 'Polish'),
	 ('pt', 'Portuguese'),
	 ('pt-br', 'Brazilian Portuguese'),
	 ('ro', 'Romanian'),
	 ('ru', 'Russian'),
	 ('sk', 'Slovak'),
	 ('sl', 'Slovenian'),
	 ('sq', 'Albanian'),
	 ('sr', 'Serbian'),
	 ('sr-latn', 'Serbian Latin'),
	 ('sv', 'Swedish'),
	 ('sw', 'Swahili'),
	 ('ta', 'Tamil'),
	 ('te', 'Telugu'),
	 ('th', 'Thai'),
	 ('tr', 'Turkish'),
	 ('tt', 'Tatar'),
	 ('uk', 'Ukrainian'),
	 ('ur', 'Urdu'),
	    ),
            )
    Adress = forms.CharField(
   	max_length=70,
        label='Adress')

    Index = forms.CharField(
   	max_length=6,
        label='Index')

    captcha = CaptchaField(
            label= ("Captcha:")
            )


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


