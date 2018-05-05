from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Survey, Question, Answer, Contactlist, Contact, UserProfile
from django.forms import DateField, ImageField


class SurveyForm(forms.ModelForm):
    deadline_Date = DateField(widget=forms.DateInput(attrs={'type': 'date'},),)

    class Meta:
        model = Survey
        fields = ['title', 'description', 'deadline_Date']

    def __init__(self, *args, **kwargs):
        self.userid = forms.CharField(widget=forms.HiddenInput())
        super(SurveyForm, self).__init__(*args, **kwargs)


class QuickSurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ['title', 'description', 'survey_pin']

    def __init__(self, *args, **kwargs):
        self.userid = forms.CharField(widget=forms.HiddenInput())
        super(QuickSurveyForm, self).__init__(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    user = UserProfile.username
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                  )
    def __init__(self,  *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(required=False)
    last_name= forms.CharField(required=False)
    date_of_birth = DateField(widget=forms.DateInput(attrs={'type': 'date'},), required=False)
    profile = ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'date_of_birth',
            'description',
            'profile',
        )


class TextQuestionForm(forms.ModelForm):
    image = ImageField()

    class Meta:
        model = Question
        fields = ['image', 'description']

    def __init__(self, *args, **kwargs):
        self.surveyid = forms.CharField(widget=forms.HiddenInput())
        self.type = 'Text'
        super(TextQuestionForm, self).__init__(*args, **kwargs)


class RadioQuestionForm(forms.ModelForm):
    image = ImageField()

    class Meta:
        model = Question
        fields = ['image', 'description', 'choices']

    def __init__(self, *args, **kwargs):
        self.type = 'Multiple Choice'
        self.surveyid = forms.CharField(widget=forms.HiddenInput())

        super(RadioQuestionForm, self).__init__(*args, **kwargs)


class TrueOrFalseQuestionForm(forms.ModelForm):
    image = ImageField()

    class Meta:
        model = Question
        fields = ['image', 'description']

    def __init__(self, *args, **kwargs):
        self.surveyid = forms.CharField(widget=forms.HiddenInput())
        super(TrueOrFalseQuestionForm, self).__init__(*args, **kwargs)


class RangeQuestionForm(forms.ModelForm):
    image = ImageField()

    class Meta:
        model = Question
        fields = ['image', 'description']

    def __init__(self, *args, **kwargs):
        self.surveyid = forms.CharField(widget=forms.HiddenInput())
        super(RangeQuestionForm, self).__init__(*args, **kwargs)


class AnswerForm(forms.ModelForm):

    class Meta:
       model = Answer
       fields = ['answer']

    def __init__(self, *args, **kwargs):
        self.question_id = forms.CharField(widget=forms.HiddenInput())
        super(AnswerForm, self).__init__(*args, **kwargs)


class ContactListForm(forms.ModelForm):

    class Meta:
        model = Contactlist
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.userid = forms.CharField(widget=forms.HiddenInput())
        super(ContactListForm, self).__init__(*args, **kwargs)

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.contactlistid = forms.CharField(widget=forms.HiddenInput())
        super(ContactForm, self).__init__(*args, **kwargs)