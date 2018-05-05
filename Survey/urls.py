from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Survey'

urlpatterns = [
    url(r'^survey-form/type/$', views.surveytype, name='survey-type'),
    url(r'^survey-form/normal/$', views.SurveyCreate.as_view(), name='normal-survey-create'),
    url(r'^survey-form/quick/$', views.QuickSurveyCreate.as_view(), name='quick-survey-create'),
    url(r'^survey-form/(?P<id>[0-9]+)/quick/link/$', views.linkforquicksurvey, name='link-quick-survey'),
    url(r'^survey-form/normal/nocontacts/$', views.needcontactfornormalsurvey, name='survey-normal-no-contact'),
    url(r'^add-questions/(?P<id>[0-9]+)/', views.index10, name='add-question'),
    url(r'^contactlist-form/$', views.ContactListCreate.as_view(), name='contactlist-create'),
    url(r'^add-contacts/(?P<contactlistid>[0-9]+)/$', views.index11, name='add-contact'),
    url(r'^contact-form/(?P<contactlistid>[0-9]+)/$', views.ContactCreate.as_view(), name='contact-form'),
    url(r'^add-radio-questions/(?P<id>[0-9]+)', views.QuestionRadioCreate.as_view(), name='radio-question-create'),
    url(r'^add-text-questions/(?P<id>[0-9]+)', views.QuestionTextCreate.as_view(), name='text-question-create'),
    url(r'^add-true-or-false-questions/(?P<id>[0-9]+)', views.QuestionTrueFalseCreate.as_view(), name='true-or-false-question-create'),
    url(r'^add-range-questions/(?P<id>[0-9]+)', views.QuestionRangeCreate.as_view(), name='range-question-create'),
    url(r'^(?P<id>[0-9]+)/answerpage/(?P<question_id>[0-9]+)/(?P<tokenid>[0-9]+)/(?P<tokenpinURL>[\w\-]+)$', views.AnswerCreate.as_view(), name='answerpage'),
    url(r'^(?P<id>[0-9]+)/answerpage/redirect-to-next-question/(?P<question_id>[0-9]+)/(?P<tokenid>[0-9]+)/$', views.gotonextquestion, name='gotonextquestion'),
    url(r'^(?P<id>[0-9]+)/answerpage/(?P<question_id>[0-9]+)/$', views.QuickAnswerCreate.as_view(), name='quickanswerpage'),
    url(r'^(?P<id>[0-9]+)/delete_question/(?P<question_id>[0-9]+)/$', views.delete_question, name='delete_question'),
    url(r'^delete_contact/(?P<contactlistid>[0-9]+)/(?P<contactid>[0-9]+)/$', views.delete_contact_during, name='delete-contact-during'),
    url(r'^contacttoinvite/(?P<id>[0-9]+)/$', views.ContactToInvite, name='ContactToInvite'),
    url(r'^waytoinvite/(?P<id>[0-9]+)/$', views.waytoinvite, name='waytoinvite'),
    url(r'^inviteindividually/(?P<id>[0-9]+)/$', views.inviteindividually, name='inviteindividually'),
    url(r'^inviteindividually/(?P<id>[0-9]+)/(?P<contactlistid>[0-9]+)/$', views.inviteindividuallylist, name='inviteindividuallylist'),
    url(r'^enterpin/(?P<id>[0-9]+)/$', views.enterpin, name='enterpin'),
    url(r'^verifyToken/(?P<id>[0-9]+)/$', views.verifyToken, name='verifyToken'),
    url(r'^(?P<id>[0-9]+)/inviteInd/(?P<contact_id>[0-9]+)/$', views.inviteInd, name='inviteInd'),
    url(r'^(?P<id>[0-9]+)/invitebylist/$', views.ByList, name='ByList'),
    url(r'^(?P<id>[0-9]+)/invitebylist/(?P<contactlistid>[0-9]+)/$', views.inviteByList, name='inviteByList'),
    url(r'^contacttoinvite/(?P<id>[0-9]+)/$', views.ContactToInvite, name='ContactToInvite'),

    url(r'^joincontactlist/(?P<userid>[0-9]+)/(?P<contactlistid>[0-9]+)/$', views.ContactCreateFromLink.as_view(), name='contact-from-link'),
    url(r'^thankyouforjoining/(?P<contactlistid>[0-9]+)/$', views.index12, name='thank-you-for-joining-contactlist'),

    url(r'^enterpin/(?P<id>[0-9]+)/$', views.enterpin, name='enterpin'),
    url(r'^verifyToken/(?P<id>[0-9]+)/$', views.verifyToken, name='verifyToken'),
    url(r'^(?P<id>[0-9]+)/inviteInd/(?P<contact_id>[0-9]+)/$', views.inviteInd, name='inviteInd'),
    url(r'^(?P<id>[0-9]+)/invitebylist/$', views.ByList, name='ByList'),
    url(r'^(?P<id>[0-9]+)/invitebylist/(?P<contactlistid>[0-9]+)/$', views.inviteByList, name='inviteByList'),
    url(r'^(?P<id>[0-9]+)/thankyou/', views.thankyou, name='thankyou'),
    url(r'^(?P<id>[0-9]+)/resultpage/$', views.Results.as_view(), name='result-page'),
    url(r'^(?P<id>[0-9]+)/resultpage/(?P<question_id>[0-9]+)/data/$', views.ChartData.as_view(), name='api-data'),

    url(r'^(?P<id>[0-9]+)/viewSurvey/$', views.viewSurvey, name='viewSurvey'),
    url(r'^search/$', views.search, name='search'),

    url(r'^deletesurveypage/$', views.delete_survey_page, name='Survey-delete-page'),
    url(r'^deletesurvey/(?P<id>[0-9]+)/$', views.delete_survey, name='Survey-delete'),
    url(r'^deletecontactlistpage/$', views.delete_contactlist_page, name='delete_contactlist_page'),
    url(r'^deletecontactlist/(?P<contactlistid>[0-9]+)/$', views.delete_contactlist, name='delete_contacts_list'),
    url(r'^deletecontactpage/(?P<contactlistid>[0-9]+)/$', views.delete_contact_page, name='delete_contacts_page'),
    url(r'^deletecontact/(?P<contact_id>[0-9]+)/$', views.delete_contact, name='delete_contacts'),

    url(r'^(?P<userotherid>[0-9]+)/profile/$', views.profileVisit, name='ProfileVisit'),

    url(r'^login/$', auth_views.login, {'template_name': 'NotLoggedIn/login.html'}, name='Log In'),
    url(r'^logout/', auth_views.logout, {'template_name': 'NotLoggedIn/home.html'}, name='Log Out'),
    url(r'^register/', views.register, name='Register'),
    url(r'^profile/$', views.profile, name='Profile'),
    url(r'^profile/edit/$', views.edit, name='Edit'),
    url(r'^profile/changePassword/$', views.changePassword, name='ChangePassword'),
    url(r'^password-reset/$', auth_views.password_reset, {
        'post_reset_redirect': '/Survey/password_reset/done/'
        },  name='password-reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {
        'post_reset_redirect': '/Survey/reset/done/'
        }, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]