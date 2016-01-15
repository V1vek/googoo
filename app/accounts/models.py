from django.db import models
import re
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class UserManager(BaseUserManager):

    def _create_user(self, username, email, first_name, last_name, password, is_retailer, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name,
                          is_active=False, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        # if is_retailer:
        #   user.is_active = False
        # else:
        user.is_active = True
        user.save(using=self._db)
        return user

    def _create_super_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model( email=email, is_staff=is_staff,
                          is_active=False, is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, first_name=None, last_name=None, password=None, is_retailer=False,
                    **extra_fields):
        log.info(username)
        return self._create_user(username, email, first_name, last_name, password, is_retailer, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_super_user( email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user

    def update_user_details(self, username,  first_name, last_name):
        user = User.objects.get(username=username)

        if user is not None:
            user.first_name = first_name
            user.last_name = last_name
            user.save
            return user
        return None


class User(AbstractBaseUser):
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),blank=True,
        related_name="tmp_user_set", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'), blank=True,
        related_name="tmp_user_set", related_query_name="user")
    username = models.CharField(_('username'), max_length=30, unique=True,
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    is_superuser = models.BooleanField(_('active'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    receive_newsletter = models.BooleanField(_('receive newsletter'), default=False)
    activation_key = models.CharField(max_length=40, blank="True")
    reset_password_key = models.CharField(max_length=40, blank="True")
    key_expires = models.DateTimeField(default=datetime.now())
    is_email_verified = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser