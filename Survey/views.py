from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View
from .forms import SurveyForm, TextQuestionForm, RadioQuestionForm, TrueOrFalseQuestionForm, RangeQuestionForm, AnswerForm, ContactListForm, ContactForm, RegistrationForm, EditProfileForm, QuickSurveyForm#, MultipleChoiceAnswerForm
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
import datetime
from Survey.models import Survey, Question, Token, Contact, Contactlist, Choice, UserProfile, Answer
import smtplib
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.urls import reverse

# Create your views here.


def profile(request):
    args = {'user': request.user}
    return render(request, 'LoggedIn/profile.html', args)


def loggedIn(request):
    return render(request, 'LoggedIn/profile.html')


def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/Survey/profile/')
        else:
            return redirect('/profile/changePassword')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'LoggedIn/changePassword.html', args)


def index10(request, id):
    survey = get_object_or_404(Survey, pk=id)
    return render(request, 'createSurvey.html', {'Survey': survey, 'user': request.user})


def edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            upload = form.save(commit=False)
            if request.FILES :
                upload.profile = request.FILES['profile']
            form.save()
            return redirect('/Survey/')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'LoggedIn/editProfile.html', args)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Survey/login/')
        else:
            form = RegistrationForm()
            args = {"form": form}
            return render(request, 'NotLoggedIn/signUp.html', args)
    else:
        form = RegistrationForm()
        args = {"form": form}
        return render(request, 'NotLoggedIn/signUp.html', args)


class SurveyCreate(CreateView):
    template_name = 'survey_form.html'
    form_class = SurveyForm

    def get_success_url(self):
        return reverse_lazy('Survey:add-question', args=(self.object.id,))

    def form_valid(self, form):
        survey = form.save(commit=False)
        survey.userid = self.request.user
        survey.survey_type = 'Normal'
        return super(SurveyCreate, self).form_valid(form)


class QuickSurveyCreate(CreateView):
    template_name = 'survey_form.html'
    form_class = QuickSurveyForm

    def get_success_url(self):
        return reverse_lazy('Survey:add-question', args=(self.object.id,))

    def form_valid(self, form):
        survey = form.save(commit=False)
        survey.userid = self.request.user
        survey.survey_type = 'Quick'
        return super(QuickSurveyCreate, self).form_valid(form)


def needcontactfornormalsurvey(request):
    return render(request, 'needcontactfornormalsurvey.html', {'user': request.user})


class QuestionTextCreate(CreateView):
    template_name = 'question_form.html'
    form_class = TextQuestionForm

    def get_form(self, form_class=None):
        form = super(QuestionTextCreate, self).get_form(TextQuestionForm)
        form.fields['image'].required = False
        return form

    def get_success_url(self):
        return reverse_lazy('Survey:add-question', args=(self.object.surveyid.id,))

    def form_valid(self, form):
        question = form.save(commit=False)
        survey = get_object_or_404(Survey, id=self.kwargs['id'])
        question.surveyid = survey
        question.type = 'Text'
        return super(QuestionTextCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionTextCreate, self).get_context_data(**kwargs)
        context['s_id'] = self.kwargs['id']
        return context


class QuestionRadioCreate(CreateView):
    template_name = 'question_form.html'
    form_class = RadioQuestionForm

    def get_form(self, form_class=None):
        form = super(QuestionRadioCreate, self).get_form(RadioQuestionForm)
        form.fields['image'].required = False
        return form

    def get_success_url(self):
        choices = self.object.get_choices()
        for choice in choices:
            choicee = Choice.objects.create(question=self.object, choice=choice)
            choicee.save()
            transaction.commit()
        return reverse_lazy('Survey:add-question', args=(self.object.surveyid.id,))

    def form_valid(self, form):
        question = form.save(commit=False)
        survey = get_object_or_404(Survey, id=self.kwargs['id'])
        question.surveyid = survey
        question.type = 'Multiple Choice'
        return super(QuestionRadioCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionRadioCreate, self).get_context_data(**kwargs)
        context['s_id'] = self.kwargs['id']
        return context


class QuestionTrueFalseCreate(CreateView):
    template_name = 'question_form.html'
    form_class = TrueOrFalseQuestionForm

    def get_form(self, form_class=None):
        form = super(QuestionTrueFalseCreate, self).get_form(TrueOrFalseQuestionForm)
        form.fields['image'].required = False
        return form

    def get_success_url(self):
        self.object.choices = 'True-False'
        choices = self.object.get_choices()
        for choice in choices:
            choicee = Choice.objects.create(question=self.object, choice=choice)
            choicee.save()
            transaction.commit()
        return reverse_lazy('Survey:add-question', args=(self.object.surveyid.id,))

    def form_valid(self, form):
        question = form.save(commit=False)
        survey = get_object_or_404(Survey, id=self.kwargs['id'])
        question.surveyid = survey
        question.type = 'True or False'
        return super(QuestionTrueFalseCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionTrueFalseCreate, self).get_context_data(**kwargs)
        context['s_id'] = self.kwargs['id']
        return context


class QuestionRangeCreate(CreateView):
    template_name = 'question_form.html'
    form_class = RangeQuestionForm

    def get_form(self, form_class=None):
        form = super(QuestionRangeCreate, self).get_form(RangeQuestionForm)
        form.fields['image'].required = False
        return form

    def get_success_url(self):
        self.object.choices = 'Strongly Disagree-Disagree-Neutral-Agree-Strongly Agree'
        choices = self.object.get_choices()
        for choice in choices:
            choicee = Choice.objects.create(question=self.object, choice=choice)
            choicee.save()
            transaction.commit()
        return reverse_lazy('Survey:add-question', args=(self.object.surveyid.id,))

    def form_valid(self, form):
        question = form.save(commit=False)
        survey = get_object_or_404(Survey, id=self.kwargs['id'])
        question.surveyid = survey
        question.type = 'Range'
        return super(QuestionRangeCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionRangeCreate, self).get_context_data(**kwargs)
        context['s_id'] = self.kwargs['id']
        return context


def delete_question(request, id, question_id):
    survey = get_object_or_404(Survey, pk=id)
    question = Question.objects.get(pk=question_id)
    question.delete()
    return render(request, 'createSurvey.html', {'Survey': survey, 'user': request.user})


def thankyou(request, id):
    survey = get_object_or_404(Survey, pk=id)
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    return render(request, 'thankyou.html', {'Survey': survey, 'extended_template': extended_template})


class AnswerCreate(CreateView):
    template_name = 'answerpage.html'
    form_class = AnswerForm

    def get_success_url(self):
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        survey = get_object_or_404(Survey, id=self.kwargs['id'])

        if survey.question_set.last() == question:
            token = get_object_or_404(Token, id=self.kwargs['tokenid'])
            token.has_answered = 1
            token.save()
            return reverse_lazy('Survey:thankyou', args=(survey.id,))
        else:
            questionset = list(Question.objects.filter(surveyid=survey.id).order_by('id').values_list('id', flat=True))
            idx = questionset.index(question.id)
            idOfNext = Question.objects.filter(surveyid=survey.id).order_by('id').get(id=questionset[idx+1]).id
            nextQues = Question.objects.get(id=idOfNext)
            return reverse_lazy('Survey:answerpage', args=(survey.id, idOfNext, self.kwargs['tokenid'], self.kwargs['tokenpinURL']))

    def form_valid(self, form):
        answer = form.save(commit=False)
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        token = get_object_or_404(Token, id=self.kwargs['tokenid'])
        answer.question_id = question
        answer.token_id = token
        if question.type == 'Multiple Choice' or question.type == 'True or False' or question.type == 'Range':
            answer.answer = self.request.POST.get('answer')
        return super(AnswerCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AnswerCreate, self).get_context_data(**kwargs)
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        token = get_object_or_404(Token, id=self.kwargs['tokenid'])
        hasAns = 0
        for answer in Answer.objects.filter(question_id=question):
            if answer.token_id == token:
                hasAns = 1
        context['Survey'] = get_object_or_404(Survey, id=self.kwargs['id'])
        context['question'] = question
        context['token'] = token
        context['hasAns'] = hasAns
        context['extended_template'] = 'NotLoggedIn/base.html'
        if self.request.user.is_authenticated:
            context['extended_template'] = 'LoggedIn/base.html'
        return context


def gotonextquestion(request, id, question_id, tokenid):
    question = get_object_or_404(Question, id=question_id)
    survey = get_object_or_404(Survey, id=id)
    token = get_object_or_404(Token, id=tokenid)

    if survey.question_set.last() == question:
        token.has_answered = 1
        token.save()
        return redirect('http://127.0.0.1:8000/Survey/'+str(survey.id)+'/thankyou')
    else:
        questionset = list(Question.objects.filter(surveyid=survey.id).order_by('id').values_list('id', flat=True))
        idx = questionset.index(question.id)
        idOfNext = Question.objects.filter(surveyid=survey.id).order_by('id').get(id=questionset[idx+1]).id
        nextQues = Question.objects.get(id=idOfNext)
        tokenpinURL = token.pin.replace('-', '')
        return redirect('http://127.0.0.1:8000/Survey/' + str(survey.id) + '/answerpage/' +
                        str(idOfNext) + '/' + str(token.id) + '/' + tokenpinURL)


class QuickAnswerCreate(CreateView):
    template_name = 'quickanswerpage.html'
    form_class = AnswerForm

    def get_success_url(self):
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        survey = get_object_or_404(Survey, id=self.kwargs['id'])
        if survey.question_set.last() == question:
            return reverse_lazy('Survey:thankyou', args=(survey.id,))
        else:
            questionset = list(Question.objects.filter(surveyid=survey.id).order_by('id').values_list('id', flat=True))
            idx = questionset.index(question.id)
            idOfNext = Question.objects.filter(surveyid=survey.id).order_by('id').get(id=questionset[idx+1]).id
            nextQues = Question.objects.get(id=idOfNext)
            return reverse_lazy('Survey:quickanswerpage', args=(survey.id, idOfNext,))

    def form_valid(self, form):
        answer = form.save(commit=False)
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        answer.question_id = question
        if question.type == 'Multiple Choices' or question.type == 'True or False' or question.type == 'Range':
            answer.answer = self.request.POST.get('answer')
        return super(QuickAnswerCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuickAnswerCreate, self).get_context_data(**kwargs)
        context['Survey'] = get_object_or_404(Survey, id=self.kwargs['id'])
        context['question'] = get_object_or_404(Question, id=self.kwargs['question_id'])
        context['extended_template'] = 'NotLoggedIn/base.html'
        if self.request.user.is_authenticated:
            context['extended_template'] = 'LoggedIn/base.html'
        return context


class ContactListCreate(CreateView):
    template_name = 'contactlist_form.html'
    form_class = ContactListForm

    def get_success_url(self):
        return reverse('Survey:add-contact', args=(self.object.id,))

    def form_valid(self, form):
        contactlist = form.save(commit=False)
        contactlist.userid = self.request.user
        return super(ContactListCreate, self).form_valid(form)


class ContactCreate(CreateView):
    template_name = 'contact_form.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse_lazy('Survey:add-contact', args=(self.kwargs['contactlistid'],))

    def form_valid(self, form):
        contact = form.save(commit=False)
        contactlist = get_object_or_404(Contactlist, id=self.kwargs['contactlistid'])#id=self.request.POST.get('question_id', None))
        contact.contactlistid = contactlist
        return super(ContactCreate, self).form_valid(form)


def index11(request, contactlistid):
    contactlist = get_object_or_404(Contactlist, pk=contactlistid)
    return render(request, 'createContactList.html', {'user': request.user, 'contactlist': contactlist})


def ContactToInvite(request, id, contactlist_id):
    survey = get_object_or_404(Survey, pk=id)
    contactlist = get_object_or_404(Contactlist, pk=contactlist_id)
    return render(request, 'contactinvite.html', {'Survey': survey, 'ContactList': contactlist})


def inviteInd(request, id, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contactlist = get_object_or_404(Contactlist, pk=contact.contactlistid.id)
    survey = get_object_or_404(Survey, id=id)
    user = survey.userid
    server = 'smtp.gmail.com'
    port = 587

    token = Token.objects.create(survey_id=survey)
    token.pin = str(token.pin)

    sender = 'markdebbane@gmail.com'
    subject = 'Blindfold: Invite to ' + survey.title + ' Survey'
    body = 'Dear, Mr/Ms ' + contact.last_name + ',\n\nYou have been invited to take a survey titled ' + survey.title \
           + ' whose results will be available the ' + str(survey.deadline_Date) + 'at http://127.0.0.1:8000/Survey/' + str(survey.id) + '/resultpage/' \
           + '.\nTo take this survey, please click on this link: ' + '127.0.0.1:8000/Survey/enterpin/' + str(survey.id) + '/\nAnd enter the following token: ' + token.pin +\
           '\n\nNote that our service provides perfect anonymity, as there is no way to trace your answers back to you.'\
           + 'If you wish to know more about our service, please click on the following link: http://127.0.0.1:8000/aboutUs/\n\n' \
           + 'Best regards,\nBlindfold team.'

    session = smtplib.SMTP(server, port)

    session.ehlo()
    session.starttls()
    session.login(sender, 'Mimosa223')
    recipient = contact.email.replace('(', '').replace(')', '').replace('\'', '').replace(',','')
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient]
    headers = "\r\n".join(headers)
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)

    session.quit()
    return render(request, 'individuallylist.html', {'Survey': survey, 'user': user, 'ContactList': contactlist})


def inviteindividually(request, id):
    survey = get_object_or_404(Survey, pk=id)
    # user = get_object_or_404(UserProfile, pk=userid)
    return render(request, 'individually.html', {'Survey': survey, 'user': request.user})


def inviteindividuallylist(request, id, contactlistid):
    survey = get_object_or_404(Survey, pk=id)
    # user = get_object_or_404(UserProfile, pk=userid)
    contactlist = get_object_or_404(Contactlist, pk=contactlistid)
    return render(request, 'individuallylist.html', {'Survey': survey, 'user': request.user, 'ContactList': contactlist})


def enterpin(request, id):
    survey = get_object_or_404(Survey, pk=id)
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    if survey.survey_type == 'Quick':
        return render(request, 'enterPin.html', {'Survey': survey, 'extented_template': extended_template})
    elif survey.deadline_Date < datetime.date.today():
        return render(request, 'expiredSurvey.html', {'extented_template': extended_template})
    else:
        return render(request, 'enterPin.html', {'Survey': survey, 'extented_template': extended_template})


def verifyToken(request, id):
    survey = get_object_or_404(Survey, pk=id)
    tokenpin = request.POST.get('tokenpin')
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    if survey.survey_type == 'Normal':
        tokenlisttemp = list(survey.token_set.all().values_list('pin'))
        tokenlist = list()
        for pin in tokenlisttemp:
            tokenlist.append(str(pin).replace('(', '').replace(')', '').replace('\'', '').replace(',',''))
        if not tokenlist.__contains__(tokenpin):
            return render(request, 'wrongPin.html', {'extended_template': extended_template})
        token = get_object_or_404(Token, pin=tokenpin)
        if token.has_answered == 1:
            return render(request, 'pinUsed.html', {'extended_template': extended_template})
        else:
            tokenpinURL = tokenpin.replace('-', '')
            return redirect('http://127.0.0.1:8000/Survey/' + str(survey.id) + '/answerpage/' +
                            str(Question.objects.filter(surveyid=survey.id).first().id) + '/' + str(token.id) + '/' + tokenpinURL)
    elif tokenpin == survey.survey_pin:
        return redirect('http://127.0.0.1:8000/Survey/' + str(survey.id) + '/answerpage/' +
                        str(Question.objects.filter(surveyid=survey.id).first().id) + '/')
    else:
        return render(request, 'wrongPin.html', {'extended_template': extended_template})


def waytoinvite(request, id):
    survey = get_object_or_404(Survey, pk=id)
    return render(request, 'waytoinvite.html', {'Survey': survey, 'user': request.user})


def surveytype(request):
    return render(request, 'survey_type.html', {'user': request.user})


def linkforquicksurvey(request, id):
    survey = get_object_or_404(Survey, pk=id)
    return render(request, 'linkforquicksurvey.html', {'Survey': survey, 'user': request.user})


def invite(id, contactid):
    contact = get_object_or_404(Contact, id=contactid)
    survey = get_object_or_404(Survey, id=id)
    server = 'smtp.gmail.com'
    port = 587

    token = Token.objects.create(survey_id=survey)
    token.pin = str(token.pin)

    sender = 'markdebbane@gmail.com'
    subject = 'Blindfold: Invite to ' + survey.title + ' Survey'
    body = 'Dear, Mr/Ms ' + contact.last_name + ',\n\nYou have been invited to take a survey titled ' + survey.title \
           + ' whose results will be available the ' + str(survey.deadline_Date) + 'at http://127.0.0.1:8000/Survey/' + str(survey.id) + '/resultpage/' \
           + '.\nTo take this survey, please click on this link: ' + '127.0.0.1:8000/Survey/enterpin/' + str(survey.id) + '/\nAnd enter the following token: ' + token.pin + \
           '\n\nNote that our service provides perfect anonymity, as there is no way to trace your answers back to you.' \
           + 'If you wish to know more about our service, please click on the following link: http://127.0.0.1:8000/aboutUs/\n\n' \
           + 'Best regards,\nBlindfold team.'

    session = smtplib.SMTP(server, port)

    session.ehlo()
    session.starttls()
    session.login(sender, 'Mimosa223')
    recipient = contact.email.replace('(', '').replace(')', '').replace('\'', '').replace(',','')
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient]
    headers = "\r\n".join(headers)
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)

    session.quit()


def ByList(request, id):
    survey = get_object_or_404(Survey, pk=id)
    return render(request, 'bylist.html', {'Survey': survey, 'user': request.user})


def inviteByList(request, id, contactlistid):
    contactlist = get_object_or_404(Contactlist, pk=contactlistid)
    survey = get_object_or_404(Survey, id=id)
    for contact in contactlist.contact_set.all():
        invite(survey.id, contact.id)
    return render(request, 'waytoinvite.html', {'Survey': survey, 'user': request.user})


class Results(View):

    def get(self, request, *args, **kwargs):
        survey = get_object_or_404(Survey, id=kwargs.get('id'))
        countNotAns = 0
        extended_template = 'NotLoggedIn/base.html'
        user = None
        if request.user.is_authenticated:
            extended_template = 'LoggedIn/base.html'
            user = get_object_or_404(UserProfile, id=request.user.id)
        if survey.survey_type == 'Quick':
            return render(request, 'result-page-attempt2.html', {'Survey': survey, 'extended_template': extended_template})
        elif survey.survey_type == 'Normal':
            if survey.deadline_Date < datetime.date.today():
                return render(request, 'result-page-attempt2.html', {'Survey': survey, 'extended_template': extended_template})
            else:
                allAnswered = 1
                for token in survey.token_set.all():
                    if token.has_answered == 0:
                        countNotAns = countNotAns + 1
                        allAnswered = 0
                if allAnswered == 1:
                    return render(request, 'result-page-attempt2.html', {'Survey': survey, 'extended_template': extended_template})
                else:
                    return render(request, 'resultsnotavailabe.html', {'Survey': survey, 'countNotAns': countNotAns, 'extended_template': extended_template})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, id, question_id, format=None):
        survey = get_object_or_404(Survey, id=id)
        question = get_object_or_404(Question, id=question_id, surveyid=survey)
        answers = []
        stats = []
        type = ''

        if question.type == 'Multiple Choice' or question.type == 'True or False' or question.type == 'Range':
            for choice in question.choice_set.all():
                answers.append(choice.choice)
                stats.append(Answer.objects.filter(question_id=question, answer=choice.choice).count())
        else:
            for answer in question.answer_set.all():
                answerstr = answer.answer
                if answerstr not in answers:
                    answers.append(answer.answer)
                    stats.append(Answer.objects.filter(question_id=question, answer=answer.answer).count())

        if question.type == 'Multiple Choice':
            type = 'bar'
        elif question.type == 'True or False':
            type = 'doughnut'
        elif question.type == 'Text':
            type = 'pie'
        else:
            type = 'horizontalBar'

        data = {
            'labels': answers,
            'stats': stats,
            'type': type,
        }
        return Response(data)


def search(request):
    surveySet = []
    string = request.POST.get('search')
    extended_template = 'NotLoggedIn/base.html'
    option = 'all'
    user = None
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
        option = request.POST.get('optionSearch')
        user = get_object_or_404(UserProfile, id=request.user.id)
    if option == 'all':
        for survey in Survey.objects.all():
            if string in survey.title:
                surveySet.append(survey)
    else:
        for survey in user.survey_set.all():
            if string in survey.title:
                surveySet.append(survey)
    return render(request, 'search.html', {'surveySet': surveySet, 'user': user, 'extended_template': extended_template})


def viewSurvey(request, id):
    survey = get_object_or_404(Survey, pk=id)
    extended_template = 'NotLoggedIn/base.html'
    user = None
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
        user = get_object_or_404(UserProfile, id=request.user.id)
    return render(request, 'viewSurvey.html', {'Survey': survey, 'user': user, 'extended_template': extended_template})


class ContactCreateFromLink(CreateView):
    template_name = 'enterinfocontact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse_lazy('Survey:thank-you-for-joining-contactlist', args=(self.kwargs['contactlistid']))

    def form_valid(self, form):
        contact = form.save(commit=False)
        contactlist = get_object_or_404(Contactlist, id=self.kwargs['contactlistid'])#id=self.request.POST.get('question_id', None))
        contact.contactlistid = contactlist
        return super(ContactCreateFromLink, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactCreateFromLink, self).get_context_data(**kwargs)
        context['extended_template'] = 'NotLoggedIn/base.html'
        if self.request.user.is_authenticated:
            context['extended_template'] = 'LoggedIn/base.html'
        return context


def index12(request, contactlistid):
    contactlist = get_object_or_404(Contactlist, id=contactlistid)
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    return render(request, 'thankyouforcontact.html', {'contactlist': contactlist, 'extended_template': extended_template})


def delete_survey_page(request):
    # user = get_object_or_404(UserProfile, pk=userid)
    return render(request, 'deletesurveys.html', {'user': request.user})


def delete_survey(request, id):
    survey = Survey.objects.get(pk=id)
    survey.delete()
    return render(request, 'deletesurveys.html', {'user': request.user})


def delete_contactlist_page(request):
    return render(request, 'deletecontactslist.html', {'user': request.user})


def delete_contactlist(request, contactlistid):
    contactlist = Contactlist.objects.get(pk=contactlistid)
    contactlist.delete()
    return render(request, 'deletecontactslist.html', {'user': request.user})


def delete_contact_page(request, contactlistid):
    contactlist = get_object_or_404(Contactlist, pk=contactlistid)
    return render(request, 'deletecontactspage.html', {'user': request.user, 'contactList': contactlist})


def delete_contact(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact.delete()
    return render(request, 'deletecontactspage.html', {'user': request.user})


def delete_contact_during(request, contactlistid, contactid):
    contactlist = get_object_or_404(Contactlist, pk=contactlistid)
    contact = Contact.objects.get(pk=contactid)
    contact.delete()
    return render(request, 'createContactList.html', {'user': request.user, 'contactlist': contactlist})


def profileVisit(request, userotherid):
    userother = get_object_or_404(UserProfile, pk=userotherid)
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    return render(request, 'profile-visit.html', {'userother': userother, 'extended_templates': extended_template})