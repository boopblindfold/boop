from django.shortcuts import render

def home(request):
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    return render(request, 'home.html', {'extended_templates': extended_template})

def aboutUs(request):
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    return render(request, 'aboutUs.html', {'extended_templates': extended_template})


def contactUs(request):
    extended_template = 'NotLoggedIn/base.html'
    if request.user.is_authenticated:
        extended_template = 'LoggedIn/base.html'
    return render(request, 'contactUs.html', {'extended_templates': extended_template})


def logIn(request):
    return render(request, 'NotLoggedIn/logIn.html')


def signUp(request):
    return render(request, 'NotLoggedIn/signUp.html')

