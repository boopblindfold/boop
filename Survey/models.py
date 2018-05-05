from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Answer(models.Model):
    answer = models.CharField(max_length=200)
    question_id = models.ForeignKey('Question', models.DO_NOTHING)
    token_id = models.ForeignKey('Token', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'answer'


def validate_list(value):
    values = value.split('-')
    if len(values) < 2:
        raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")

class Question(models.Model):
    TEXT = 'Text'
    MULTIPLE_CHOICE = 'Multiple Choice'
    TRUE_FALSE = 'True or False'
    RANGE = 'Range'

    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TRUE_FALSE, 'True or False'),
        (RANGE, 'Range'),
    )

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=15, choices=QUESTION_TYPES)
    description = models.CharField(max_length=200)
    choices = models.TextField(blank=True, null=True, help_text='Provide a dash-separated list of options for this question .')
    surveyid = models.ForeignKey('Survey', models.DO_NOTHING, db_column='surveyid', blank=True, null=True)
    RangeMax = models.IntegerField(blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to='uploads/')

    class Meta:
        managed = True
        db_table = 'question'

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        choices = self.choices.split('-')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append(c)
        choices_tuple = tuple(choices_list)
        return choices_list


class Survey(models.Model):
    NORMAL = 'Normal'
    QUICK = 'Quick'

    SURVEY_TYPES = (
        (NORMAL, 'Normal'),
        (QUICK, 'Quick'),
    )

    title = models.CharField(max_length=200)
    deadline_Date = models.DateField(db_column='deadline_Date', blank=True)  # Field name made lowercase.
    description = models.TextField()
    userid = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='userid', blank=True, null=True)
    survey_pin = models.CharField(max_length=45, blank=True, null=True)
    survey_type = models.CharField(max_length=6, blank=True, null=True,  choices=SURVEY_TYPES)

    class Meta:
        managed = True
        db_table = 'survey'


class Token(models.Model):
    pin = models.CharField(db_column='pin', unique=True, max_length=100, default=uuid.uuid4)  # Field name made lowercase.
    has_answered = models.IntegerField(default=0)
    survey_id = models.ForeignKey(Survey, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'token'


class Contact(models.Model):
    email = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)
    contactlistid = models.ForeignKey('Contactlist', models.DO_NOTHING, db_column='contactlistid', blank=True, null=True)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)

    def getContact(self):
        return self

    class Meta:
        managed = True
        db_table = 'contact'


class Contactlist(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    userid = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='userid', blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'contactlist'

class Choice(models.Model):
    choice = models.CharField(max_length=45, blank=True, null=True)
    question = models.ForeignKey('Question', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'choice'


class UserManager(BaseUserManager):
    def create_user(self, f_name, l_name, email, date_of_birth, username, password=None,):
        if not email:
            msg = 'Users must have an email address'
            raise ValueError(msg)

        if not username:
            msg = 'This username is not valid'
            raise ValueError(msg)

        if not date_of_birth:
            msg = 'Please Verify Your DOB'
            # raise ValueError(msg)

        user = self.model(

        email=UserManager.normalize_email(email), username=username, date_of_birth=date_of_birth, first_name = f_name, last_name=l_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(f_name= "", l_name="", email=email, password=password, username=username, date_of_birth=None,)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def is_valid(self):
        return True


class UserProfile(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100,)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    profile = models.FileField(blank=True, upload_to='uploads/', null=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    manager = UserManager()

    class Meta:
        managed = True
        db_table = 'userprofile'

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user = UserProfile.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)