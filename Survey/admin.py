from django.contrib import admin
from .models import Survey, Question, Token, Answer, Contactlist, Contact, Choice, UserProfile

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Token)
admin.site.register(Answer)
admin.site.register(Contactlist)
admin.site.register(Contact)
admin.site.register(Choice)
admin.site.register(UserProfile)